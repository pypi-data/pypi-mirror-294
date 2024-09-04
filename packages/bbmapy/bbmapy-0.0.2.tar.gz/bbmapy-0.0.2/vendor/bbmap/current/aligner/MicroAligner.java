package aligner;

import java.util.ArrayList;

import dna.AminoAcid;
import fileIO.FileFormat;
import prok.GeneCaller;
import shared.Tools;
import stream.ConcurrentGenericReadInputStream;
import stream.Read;
import structures.ByteBuilder;
import structures.LongHashMap;

/**
 * Aligns reads to a small, single sequence reference like PhiX.
 * The reference should not have any duplicate kmers.
 * Alignment is only attempted once, at the first matching kmer.
 * This will generate a match string and return the identity.
 * 
 * @author Brian Bushnell
 * @date March 18, 2024
 *
 */
public class MicroAligner {
	
	/*--------------------------------------------------------------*/
	/*----------------        Initialization        ----------------*/
	/*--------------------------------------------------------------*/

	public MicroAligner(int k_, float minIdentity_, String path) {
		this(k_, minIdentity_, loadRef(path));
	}

	public MicroAligner(int k_, float minIdentity_, byte[] ref_) {
		this(k_, minIdentity_, ref_, indexRef(k_, ref_));
	}

	public MicroAligner(int k_, float minIdentity_, byte[] ref_, LongHashMap map_) {
		k=k_;
		k2=k-1;
		ref=ref_;
		map=map_;
		minIdentity=minIdentity_;
		maxSubFraction=1-minIdentity;
	}
	
	private static byte[] loadRef(String path) {
		ArrayList<Read> list=ConcurrentGenericReadInputStream.getReads(1, false, 
				FileFormat.testInput(path, null, false), null, null, null);
		return list.get(0).bases;
	}
	
	//TODO: Add MaskMiddle and/or hdist
	private static LongHashMap indexRef(int k, byte[] ref) {
		LongHashMap map=new LongHashMap(ref.length*2);
		byte[] bases=ref;
		
		assert(k<=32);
		
		if(bases==null || bases.length<k){return null;}
		final int bitsPerBase=2;
		final int shift=bitsPerBase*k;
		final int shift2=shift-bitsPerBase;
		final long mask=(shift>63 ? -1L : ~((-1L)<<shift));
		
		long kmer=0;
		long rkmer=0;
		int len=0;
		
		for(int i=0; i<bases.length; i++){
			final byte b=bases[i];
			long x=AminoAcid.baseToNumber[b];
			long x2=AminoAcid.baseToComplementNumber[b];
			kmer=((kmer<<2)|x)&mask;
			rkmer=((rkmer>>>2)|(x2<<shift2))&mask;

			if(x<0){
				len=0;
				kmer=rkmer=0;
			}else{
				len++;
				if(len>=k){
					long key=Tools.max(kmer, rkmer);
					int value=(key==kmer ? i : i+MINUS_CODE);
					map.put(key, value);
				}
			}
		}
		return map;
	}
	
	/*--------------------------------------------------------------*/
	/*----------------          Alignment           ----------------*/
	/*--------------------------------------------------------------*/
	
	/** Returns identity */
	public float map(Read r) {
		if(r==null || r.length()<k || r.match!=null || r.samline!=null) {return 0;}
		byte[] bases=r.bases;
		if(bases==null || bases.length<k){return 0;}
		final int bitsPerBase=2;
		final int shift=bitsPerBase*k;
		final int shift2=shift-bitsPerBase;
		final long mask=(shift>63 ? -1L : ~((-1L)<<shift));
		
		long kmer=0;
		long rkmer=0;
		int len=0;
		int offset=-1;
		int orientation=-1;
		int ivalue=-1;
		int vvalue=-1;
		
		//TODO: This loop could be replaced by the kmer list which already exists.
		for(int i=0; i<bases.length && orientation<0; i++){
			final byte b=bases[i];
			long x=AminoAcid.baseToNumber[b];
			long x2=AminoAcid.baseToComplementNumber[b];
			kmer=((kmer<<2)|x)&mask;
			rkmer=((rkmer>>>2)|(x2<<shift2))&mask;

			if(x<0){
				len=0;
				kmer=rkmer=0;
			}else{
				len++;
				if(len>=k /*&& ((i&1)==0)*/){
					long key=Tools.max(kmer, rkmer);
					int value=map.get(key);
					if(value>=0) {
						ivalue=i;
						vvalue=value;
						
						if(value>=MINUS_CODE) {
							value-=MINUS_CODE;
							if(key==kmer) {
								orientation=1;
								offset=value-k2-(bases.length-i-1);
							}else {
								assert(key==rkmer);
								orientation=2;
								offset=value-i;
							}
						}else {
							if(key==kmer) {
								orientation=0;
								offset=value-i;
							}else {
								assert(key==rkmer);
								orientation=3;
								offset=value-k2-(bases.length-i-1);
							}
						}
					}
				}
			}
		}
		if(orientation<0) {return 0;}
		//				System.err.println("i="+ivalue+", v="+vvalue+
		//						", offset="+offset+", orientation="+orientation);
		final float id;
		int pad=5;
		if(orientation==1 || orientation==3) {
			r.reverseComplement();
			id=align(r, ref, offset, offset+r.length(), pad, minIdentity);
			r.reverseComplement();
		}else {
			id=align(r, ref, offset, offset+r.length(), pad, minIdentity);
		}
		return id;
	}
	
	public float align(Read r, byte[] ref, int a, int b, int pad, float minIdentity){
		int subs=quickAlign(r, ref, a);
		if(subs<4) {
//			assert(r.match!=null);
			return (r.length()-subs)/Tools.max(1f, r.length());
		}
		
		SingleStateAlignerFlat2 ssa=GeneCaller.getSSA();
		a=Tools.max(0, a-pad);
		b=Tools.min(ref.length-1, b+pad);
		int[] max=ssa.fillUnlimited(r.bases, ref, a, b, 0);
		if(max==null){return 0;}
		
		final int rows=max[0];
		final int maxCol=max[1];
		final int maxState=max[2];
		
		//returns {score, bestRefStart, bestRefStop} 
		//padded: {score, bestRefStart, bestRefStop, padLeft, padRight};
		int[] score=ssa.score(r.bases, ref, a, b, rows, maxCol, maxState);
		int rstart=score[1];
		int rstop=score[2];
		r.start=rstart;
		r.stop=rstop;
		
		byte[] match=ssa.traceback(r.bases, ref, a, b, rows, maxCol, maxState);
		float id=Read.identity(match);
		
		if(id<minIdentity) {return id;}//Probably not phix
		r.match=match;
		
		return id;
	}
	
	public int quickAlign(Read read, byte[] ref, int a) {
		byte[] bases=read.bases;
		ByteBuilder buffer=buffer();
		buffer.clear();
		int subs=0, ns=0;
		for(int i=0, j=a; i<bases.length; i++, j++) {
			if(j<0 || j>=ref.length) {
				buffer.append('C');
			}else {
				final byte q=bases[i], r=ref[j];
				if(q=='N') {
					buffer.append('N');
					ns++;
				}else if(r=='N' || r==q) {
					buffer.append('m');
				}else {
					buffer.append('S');
					subs++;
				}
			}
		}
		if(subs<4) {
			read.match=buffer.toBytes();
		}
		return subs;
	}
	
	/*--------------------------------------------------------------*/
	/*----------------           Getters            ----------------*/
	/*--------------------------------------------------------------*/
	
	private static final ByteBuilder buffer() {
		ByteBuilder buffer=bufferHolder.get();
		if(buffer==null) {
			buffer=new ByteBuilder();
			bufferHolder.set(buffer);
		}
		return buffer;
	}
	
	/*--------------------------------------------------------------*/
	/*----------------            Fields            ----------------*/
	/*--------------------------------------------------------------*/

	final float minIdentity;
	final float maxSubFraction;
	final int k;
	final int k2;
	final byte[] ref;
	final LongHashMap map;
	private static final ThreadLocal<ByteBuilder> bufferHolder=new ThreadLocal<ByteBuilder>();
//	final ByteBuilder buffer=new ByteBuilder();
	
	//Indicates the position is on the minus strand
	private static final int MINUS_CODE=1000000000;
}
