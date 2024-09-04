package barcode;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.LinkedHashSet;

import shared.Shared;
import shared.Timer;
import shared.Tools;
import structures.ByteBuilder;
import template.Accumulator;
import template.ThreadWaiter;

/**
 * Tracks data about bar code mismatches by position.
 * Used for demultiplexing.
 * 
 * @author Brian Bushnell
 * @date March 22, 2024
 *
 */
public class PCRMatrixHDist_old extends PCRMatrix implements Accumulator<PCRMatrixHDist_old.PopThread> {

	/*--------------------------------------------------------------*/
	/*----------------         Constructor          ----------------*/
	/*--------------------------------------------------------------*/
	
	public PCRMatrixHDist_old(int length1_, int length2_, int delimiter_, boolean hdistSum_) {
		super(length1_, length2_, delimiter_, hdistSum_);
	}

	/*--------------------------------------------------------------*/
	/*----------------           Parsing            ----------------*/
	/*--------------------------------------------------------------*/
	
	public static boolean parseStatic(String arg, String a, String b){
		if(a.equals("maxhdist") || a.equals("hdist") || a.equals("maxhdist0") || a.equals("hdist0")){
			maxHDist0=Integer.parseInt(b);
		}else if(a.equals("clearzone") || a.equals("cz") || a.equals("clearzone0") || a.equals("cz0")){
			clearzone0=Integer.parseInt(b);
		}else if(a.equals("parse_flag_goes_here")){
			//set something
		}else{
			return false;
		}
		return true;
	}
	
	@Override
	public boolean parse(String arg, String a, String b) {
		return false;
	}
	
	public static void postParseStatic(){}
	
	/*--------------------------------------------------------------*/
	/*----------------            HDist             ----------------*/
	/*--------------------------------------------------------------*/
	
	@Override
	public Barcode findClosest(String s) {
		return findClosest(s, maxHDist0, clearzone0);
	}
	
	public Barcode findClosest(String q, int maxHDist, int clearzone) {
		assert(!expectedList.isEmpty());
		Barcode best=null, best2=null;
		
//		Barcode best=expectedMap.get(q);
//		if(best!=null) {return best;}
		
		int hdist=hdist(length1, length2);
		int hdist2=hdist;
		assert(best==null);
		
		for(Barcode b : expectedList) {
			final int d=hdist(q, b.name);
			if(d<hdist2) {
				best2=b;
				hdist2=d;
				if(d<hdist) {
					best2=best;
					hdist2=hdist;
					best=b;
					hdist=d;
				}
			}
		}
		if(best==null || hdist>maxHDist) {return null;}
		if(hdist+clearzone>hdist2) {return null;}
		return best;
	}

	@Override
	public void makeProbs() {
		throw new RuntimeException("This class does not support this method.");
	}

	@Override
	public void initializeData() {
		//Do nothing
	}
	
	@Override
	public void refine(Collection<Barcode> codeCounts, long minCount) {
		//Do nothing
	}
	
	@Override
	public HashMap<String, String> makeAssignmentMap(Collection<Barcode> codeCounts, long minCount) {
		Timer t=new Timer();
		assert(expectedList!=null && expectedList.size()>0) : expectedList;
		assert(codeCounts!=null);
		ArrayList<Barcode> list=highpass(codeCounts, minCount);
		HashMap<String, String> map=new HashMap<String, String>(Tools.max(200, list.size()/10));
		totalCounted=totalAssigned=totalAssignedToExpected=0;
		final long ops=list.size()*(long)expectedList.size();
		final int threads=Tools.min(Shared.threads(), matrixThreads);
		if(list.size()<2 || ops<100000 || threads<2) {//Singlethreaded mode
			for(Barcode query : list) {
				final String s=query.name;
				assert(s.length()==counts.length);
				Barcode ref=findClosest(s);
				final long count=query.count();
				totalCounted+=count;
				if(ref!=null) {
					totalAssigned+=count;
					if(ref.expected==1) {
						totalAssignedToExpected+=count;
						map.put(s, ref.name);
					}
				}
			}
		}else {
			populateCountsMT(list, maxHDist0, clearzone0, map);
		}
		t.stop();
		if(verbose) {
			System.err.println(String.format("Final Assignment Rate:  \t%.4f\t%.4f", 
					assignedFraction(), expectedFraction())+"\t"+t.timeInSeconds(2)+"s");
		}
		return map;
	}

	/*--------------------------------------------------------------*/
	/*----------------          Populating          ----------------*/
	/*--------------------------------------------------------------*/
	
	@Override
	public void populateCounts(ArrayList<Barcode> list, long minCount) {
		assert(minCount<2) : "TODO";
		assert(expectedList!=null && expectedList.size()>0) : expectedList;
		assert(list!=null);
		final long ops=list.size()*(long)expectedList.size();
		if(list.size()<2 || ops<100000 || Shared.threads()<2) {
			populateCountsST(list, maxHDist0, clearzone0);
		}else {
			populateCountsMT(list, maxHDist0, clearzone0, null);
		}
	}

	private void populateCountsST(ArrayList<Barcode> countList,
			int maxHDist, int clearzone) {
		for(Barcode query : countList) {
			final String s=query.name;
			assert(s.length()==counts.length);
			Barcode ref=findClosest(s, maxHDist, clearzone);
			add(s, ref, query.count());
		}
	}

	private void populateCountsMT(ArrayList<Barcode> list,
			int maxHDist, int clearzone, HashMap<String, String> map) {
		//Do anything necessary prior to processing
		
		//Determine how many threads may be used
		final int threads=Tools.mid(1, Shared.threads(), list.size()/8);
		
		//Fill a list with PopThreads
		ArrayList<PopThread> alpt=new ArrayList<PopThread>(threads);
		for(int i=0; i<threads; i++){
			alpt.add(new PopThread(list, maxHDist, clearzone, map, i, threads));
		}
		
		//Start the threads and wait for them to finish
		boolean success=ThreadWaiter.startAndWait(alpt, this);
		errorState&=!success;
		
		//Do anything necessary after processing
		if(localCounts && map!=null) {
			for(PopThread pt : alpt) {
				synchronized(pt) {map.putAll(pt.map);}
			}
		}
	}
	
	public void populateUnexpected() {
		assert(length1>0 && length2>0) : "This is only for dual barcodes.";
		LinkedHashSet<String> set=new LinkedHashSet<String>();
		LinkedHashSet<String> set1=new LinkedHashSet<String>();
		LinkedHashSet<String> set2=new LinkedHashSet<String>();
//		ArrayList<String> leftList=new ArrayList<String>(expectedList.size());
//		ArrayList<String> rightList=new ArrayList<String>(expectedList.size());
		for(Barcode b : expectedList) {
			assert(b.expected==1);
			assert(!set.contains(b.name)) :"Duplicate expected barcode: "+b.name+"; set.size="+set.size();
			set.add(b.name);
			String code1=b.name.substring(0, length1);
			String code2=b.name.substring(start2);
			set1.add(code1);
			set2.add(code2);
		}
		
		ByteBuilder bb=new ByteBuilder(length);
		for(String code1 : set1) {
			for(String code2 : set2) {
				bb.clear();
				bb.append(code1);
				if(delimiter>0) {bb.append((byte)delimiter);}
				bb.append(code2);
				String code=bb.toString();
				if(!set.contains(code)) {
					set.add(code);
					Barcode b=new Barcode(code, 0, 0);
					b.frequency=1;
					expectedList.add(b);
					//I could add it to the map here too, but it's not necessary
				}
			}
		}
	}
	
	@Override
	public ByteBuilder toBytesProb(ByteBuilder bb) {
		throw new RuntimeException("This class does not support this method.");
	}
	
	protected boolean valid() {return true;}
	
	/*--------------------------------------------------------------*/

	final class PopThread extends Thread {

		public PopThread(ArrayList<Barcode> list_,
				int maxHDist_, int clearzone_, HashMap<String, String> map_, int tid_, int threads_) {
			list=list_;
			maxHDist=maxHDist_;
			clearzone=clearzone_;
			tid=tid_;
			threads=threads_;
			map=(map_==null ? null : localCounts ? new HashMap<String, String>() : map_);
			countsT=(localCounts ? new long[length][5][5] : null);
		}

		@Override
		public void run() {
			for(int i=tid; i<list.size(); i+=threads) {
				Barcode query=list.get(i);
				final String s=query.name;
				assert(s.length()==length);
				Barcode ref=findClosest(s, maxHDist, clearzone);
				if(localCounts) {
					addT(s, ref, query.count());
					if(map!=null && ref!=null && ref.expected==1) {map.put(s, ref.name);}
				}else {
					synchronized(counts) {
						add(s, ref, query.count());
						if(map!=null && ref!=null && ref.expected==1) {map.put(s, ref.name);}
					}
				}
			}
		}
		
		public void addT(String query, Barcode ref, long count) {
			assert(ref==null || ref.length()==countsT.length);
			for(int i=0; i<query.length(); i++) {
				final int q=query.charAt(i), r=(ref==null ? 'N' : ref.charAt(i));
				final byte xq=baseToNumber[q], xr=baseToNumber[r];
				countsT[i][xq][xr]+=count;
			}
			totalCountedT+=count;
			if(ref!=null) {
				ref.incrementSync(count);
				totalAssignedT+=count;
				totalAssignedToExpectedT+=ref.expected*count;
			}
		}

		final ArrayList<Barcode> list;
		final int maxHDist;
		final int clearzone;
		final int tid;
		final int threads;
		final HashMap<String, String> map;
		
		final long[][][] countsT;
		long totalCountedT;
		long totalAssignedT;
		long totalAssignedToExpectedT;
	}

	@Override
	public final void accumulate(PopThread t) {
		if(localCounts) {
			synchronized(t) {
				Tools.add(counts, t.countsT);
				totalCounted+=t.totalCountedT;
				totalAssigned+=t.totalAssignedT;
				totalAssignedToExpected+=t.totalAssignedToExpectedT;
			}
		}
	}

	@Override
	public boolean success() {
		return !errorState;
	}
	
	/*--------------------------------------------------------------*/
	
	static int maxHDist0=1;
	static int clearzone0=1;
	
}
