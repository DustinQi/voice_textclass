package mypackage;   
import java.io.File;    
import java.io.FileWriter;
import java.io.IOException;
 

public class saveAsTxt{
	public void saveReserved1(String element, int i){
		String filename = "d:/Users/qimy/Desktop/qmy/training_set/8_wrongplace/"+ String.valueOf(i) + ".txt";
		File nf = new File(filename);
		//新建txt文件，并将字符串写入此txt文件
		if(!nf.exists()){
			try{
				nf.createNewFile();
				FileWriter wt = new FileWriter(nf);
				wt.write(element);
				wt.flush();
				wt.close();
			}catch(IOException e){
				e.printStackTrace();
			}		
		}
		else {
			System.out.println("create file failed, the file has existed...");
		}
		
		
		
	}
}