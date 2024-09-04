package hiseq;

import align2.QualityTools;
import barcode.BarcodeStats;
import dna.AminoAcid;
import shared.Tools;
import stream.Read;
import stream.SamLine;
import structures.ByteBuilder;

public class MicroTile {

	public MicroTile(){}

	public MicroTile(int lane_, int tile_, int x1_, int x2_, int y1_, int y2_){
		lane=lane_;
		tile=tile_;
		x1=x1_;
		x2=x2_;
		y1=y1_;
		y2=y2_;
	}
	
	void process(){
		if(tracker!=null){tracker.process();}
	}
	
	public boolean contains(int x, int y){
		return x>=x1 && x<=x2 && y>=y1 && y<=y2;
	}
	
	@Override
	public String toString(){
		return lane+", "+tile+", "+x1+", "+x2+", "+y1+", "+y2;
	}
	
	public double averageQuality(){
		return readCount==0 ? 0 : qualitySum/readCount;
	}
	
	public double percentErrorFree(){
		return readCount==0 ? 0 : probErrorFreeSum/readCount;
	}
	
	public double alignmentRate(){
		return readCount==0 ? 0 : alignedReadCount/(double)readCount;
	}
	
	//Small sample sizes will drift toward 20. 
	public double trueQuality(){
		double e=baseErrorCount+4;
		double b=alignedBaseCount+400;
		double prob=e/b;
		double phred=QualityTools.probErrorToPhredDouble(prob);
//		System.err.println(baseErrorCount+", "+alignedBaseCount+", "+prob+", "+phred);
		return phred;
	}
	
	//Small sample sizes will drift toward 0.1. 
	public double readErrorRate(){
		double e=readErrorCount+1;
		double b=alignedReadCount+10;
		double rate=e/b;
		return rate;
	}
	
	public double readInsRate(){
//		System.err.println(alignedReadCount+", "+readInsCount+", "+
//		(readInsCount/(double)alignedReadCount));
		if(alignedReadCount==0) {return 0;}
//		double e=readInsCount+0.01;
//		double b=alignedReadCount+10;
		double e=readInsCount;
		double b=alignedReadCount;
		double rate=e/b;
		return rate;
	}
	 
	public double readDelRate(){
		if(alignedReadCount==0) {return 0;}
//		double e=readDelCount+0.01;
//		double b=alignedReadCount+10;
		double e=readDelCount;
		double b=alignedReadCount;
		double rate=e/b;
		return rate;
	}
	 
	public double kmerErrorRateR(){
		if(readCount==0) {return 0;}
		double e=kmerReadErrorCount;
		double b=readCount;
		double rate=e/b;
		return rate;
	}
	 
	public double kmerErrorRateB(){
		if(readCount==0) {return 0;}
		double e=kmerBaseErrorCount;
		double b=readCount;
		double rate=e/b;
		return rate;
	}
	
	public double hitPercent(){
		long count=kmerCount();
		return count==0 ? 0 : hits*100.0/count;
	}
	
	public double uniquePercent(){
		long count=kmerCount();
		return count==0 ? 0 : misses*100.0/count;
	}
	
	public double depth(){
		long count=kmerCount();
		return depthSum*1.0/count;
	}
	
	public double avgG(){
		return tracker==null ? 0 : tracker.avg('G');
	}
	
	public double maxG(){
		return tracker==null ? 0 : tracker.max('G');
	}

	public long kmerCount(){return hits+misses;}
	
	public void add(MicroTile mt) {
		hits+=mt.hits;
		misses+=mt.misses;
		depthSum+=mt.depthSum;
		readCount+=mt.readCount;
		alignedReadCount+=mt.alignedReadCount;
		alignedBaseCount+=mt.alignedBaseCount;
		readErrorCount+=mt.readErrorCount;
		baseErrorCount+=mt.baseErrorCount;
		kmerReadErrorCount+=mt.kmerReadErrorCount;
		kmerBaseErrorCount+=mt.kmerBaseErrorCount;
		readInsCount+=mt.readInsCount;
		readDelCount+=mt.readDelCount;
		qualitySum+=mt.qualitySum;
		probErrorFreeSum+=mt.probErrorFreeSum;

		for(int i=0; i<acgtn.length; i++){
			acgtn[i]+=mt.acgtn[i];
		}
		homoPolyGCount+=mt.homoPolyGCount;
		homoPolyGSum+=mt.homoPolyGSum;
		if(TRACK_CYCLES){
			tracker.add(mt.tracker);
		}
		Tools.add(barcodeHDist, mt.barcodeHDist);
		barcodeHDistSum+=mt.barcodeHDistSum;
	}
	
	public void add(Read r){
		if(r==null){return;}
		final int len=r.length();
		if(len<1){return;}
		final SamLine sl=r.samline;
		final byte[] match=r.match;
		
		readCount++;
		qualitySum+=r.avgQualityByProbabilityDouble(true, len);
		probErrorFreeSum+=100*r.probabilityErrorFree(true, len);
		
		
//		if(r.mapped() || (sl!=null && sl.mapped()){alignedRead
		
		if(match!=null) {
			int bc=r.countAlignedBases();
			if(bc>0) {
				alignedReadCount++;
				alignedBaseCount+=bc;
				int errors=r.countErrors();
				readErrorCount+=(errors>0 ? 1 : 0);
				baseErrorCount+=errors;
				int[] mSCNID=Read.countMatchEvents(match);
				readInsCount+=(mSCNID[4]>0 ? 1 : 0);
				readDelCount+=(mSCNID[5]>0 ? 1 : 0);
			}
		}else if(sl!=null && sl.mapped()) {
			alignedReadCount++;
		}
		
		final byte[] bases=r.bases;
		int maxPolyG=0, currentPolyG=0;
		for(int i=0; i<len; i++){
			byte b=bases[i];
			byte x=AminoAcid.baseToNumberACGTN[b];
			acgtn[x]++;
			if(b=='G'){
				currentPolyG++;
				maxPolyG=Tools.max(currentPolyG, maxPolyG);
			}else{
				currentPolyG=0;
			}
		}
		homoPolyGCount+=(maxPolyG>=MIN_POLY_G ? 1 : 0);
		homoPolyGSum+=maxPolyG;
		if(TRACK_CYCLES){
			tracker.add(r);
		}
	}
	
	public static String header() {
		if(shortHeader) {
			return "lane\ttile\tx1\tx2\ty1\ty2"
					+ "\treads\talnRead\talnBase\terrAlnR\terrAlnB"
					+ "\terrKR\terrKB"
					+ "\tinsCnt\tdelCnt"
					+ "\tunique\tavQscor\tprobEF\tdepth"
					+ "\talnRate\ttruQual"
					+ "\teKRRate\teKBRate\tinsRate\tdelRate"
					+ "\tdiscard"
					+ "\tA\tC\tG\tT\tN\tpolyG\tplyGLen"
					+ "\tbcBadRt\thDist0\thDist1\thDist2\thDist3+\thDAvg";
		}
		return "lane\ttile\tx1\tx2\ty1\ty2"
		+ "\treads\talignedRead\talignedBase\treadsAlignedWithErrors\talignedErrorCount"
		+ "\treadsWithKmerErrors\tkmerErrorCount"
		+ "\tinsertionCount\tdeletionCount"
		+ "\tuniqueKmerRate\tavgQscore\tprobErrorFree\tdepth"
		+ "\talignmentRate\ttrueQuality"
		+ "\treadsWithKmerErrorsRate\tkmerErrorsPerRead\tinsertionRate\tdeletionRate"
		+ "\tdiscard"
		+ "\tA\tC\tG\tT\tN\tpolyG_Count\tpolyG_Length"
		+ "\tbadBarcodeRate\texpectedBarcodes\tbarcodesWithHammingDist1"
		+ "\tbarcodesWithHammingDist2\tbarcodesWithHammingDist3+\tavgHDist";
	}
	
	public void toText(ByteBuilder bb){
		bb.append(lane).tab();
		bb.append(tile).tab();
		bb.append(x1).tab();
		bb.append(x2).tab();
		bb.append(y1).tab();
		bb.append(y2).tab();
		
		bb.append(readCount).tab();
		bb.append(alignedReadCount).tab();//new
		bb.append(alignedBaseCount).tab();//new
		bb.append(readErrorCount).tab();//new
		bb.append(baseErrorCount).tab();//new
		bb.append(kmerReadErrorCount).tab();//new
		bb.append(kmerBaseErrorCount).tab();//new
		bb.append(readInsCount).tab();//new
		bb.append(readDelCount).tab();//new
		
		bb.append(uniquePercent(), 4).tab();
		bb.append(averageQuality(), 4).tab();
		bb.append(percentErrorFree(), 4).tab();
		double depth=depth();
		if(depth>10000) {
			bb.append((long)Math.round(depth)).tab();
		}else {
			bb.append(depth, depth>=100 ? 2 : 4).tab();
		}
		bb.append(alignmentRate(), 5).tab();//new
		bb.append(trueQuality(), 4).tab();//new
		bb.append(kmerErrorRateR(), 5).tab();//new
		bb.append(kmerErrorRateB(), 5).tab();//new
		bb.append(readInsRate(), 5).tab();//new
		bb.append(readDelRate(), 5).tab();//new
		bb.append(discard);
		
		for(int i=0; i<5; i++){
			bb.tab().append(acgtn[i]);
		}
		bb.tab().append(homoPolyGCount);
		bb.tab().append(homoPolyGSum);
		
		long barcodes=Tools.sum(barcodeHDist);
		long bad=barcodes-barcodeHDist[0];
		double invBarcodes=1.0/(Tools.max(1.0, barcodes));
		bb.tab().append(String.format("%.5f", bad*invBarcodes));
		for(int i=0; i<barcodeHDist.length; i++) {
			bb.tab().append(barcodeHDist[i]);
		}
		bb.tab().append(String.format("%.4f", barcodeHDistSum*invBarcodes));//avg hdist
		
		bb.nl();
	}
	
	public long hits;
	public long misses;
	public long depthSum;
	public long readCount;
	public long alignedReadCount;
	public long alignedBaseCount;
	public long readErrorCount;//Reads aligned with errors
	public long baseErrorCount;//Bases aligned with errors
	public long kmerReadErrorCount;//Reads with errors detected
	public long kmerBaseErrorCount;//Bases detected as errors
	public long readInsCount;//Number of reads containing insertions
	public long readDelCount;//Number of reads containing deletions
	public double qualitySum;
	public double probErrorFreeSum;
	
	public int discard=0;
	
	public int lane;
	public int tile;
	public int x1, x2;
	public int y1, y2;
	
	long[] barcodeHDist=new long[4];
	long barcodeHDistSum=0;
	
	//TODO: These fields are not currently parsed.
	public long[] acgtn=new long[5];
	public long homoPolyGCount;
	public long homoPolyGSum;
	
	public final CycleTracker tracker=TRACK_CYCLES ? new CycleTracker() : null;

	public static int MIN_POLY_G=25;
	public static boolean TRACK_CYCLES=false;
	public static boolean shortHeader=true;
	
}
