package hiseq;

import java.util.ArrayList;

import structures.ByteBuilder;

public class Tile {
	
	public Tile(int lane_, int tile_){
		lane=lane_;
		tile=tile_;
	}
	
	public MicroTile get(int x, int y){
		final int xindex=x/xSize, yindex=y/ySize;
		ArrayList<MicroTile> ylist=getIndex(xindex);
		while(yindex>=ylist.size()){ylist.add(null);}
		MicroTile mt=ylist.get(yindex);
		if(mt==null){
			mt=new MicroTile(lane, tile, xindex*xSize, (xindex+1)*xSize-1, yindex*ySize, (yindex+1)*ySize-1);
			ylist.set(yindex, mt);
		}
		assert(mt.contains(x,  y)) : x+", "+y+", "+xindex+", "+yindex+", "+mt;
		return mt;
	}
	
	private ArrayList<MicroTile> getIndex(int xindex){
		while(xindex>=xlist.size()){xlist.add(new ArrayList<MicroTile>());}
		ArrayList<MicroTile> ylist=xlist.get(xindex);
		return ylist;
	}
	
	@Override
	public String toString(){
		ByteBuilder bb=new ByteBuilder();
		for(ArrayList<MicroTile> ylist : xlist){
			if(ylist!=null){
				for(MicroTile mt : ylist){
					if(mt!=null){
						mt.toText(bb);
					}
				}
			}
		}
		return bb.toString();
	}
	
	public void add(Tile tb) {
		for(ArrayList<MicroTile> x : tb.xlist) {
			for(MicroTile mtb : x) {
//				System.err.println("Adding mt "+mtb.x1+" "+mtb.y1);
				if(mtb!=null) {
					MicroTile mta=get(mtb.x1, mtb.y1);
					mta.add(mtb);
				}
			}
		}
	}
	
	
	public ArrayList<ArrayList<MicroTile>> xlist=new ArrayList<ArrayList<MicroTile>>();
	
	public int lane;
	public int tile;
	public static int xSize=500;
	public static int ySize=500;
}
