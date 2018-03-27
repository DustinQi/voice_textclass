package mypackage;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import mypackage.saveAsTxt;

 /**
  * 获取语音识别结果文本
  * @author dustin
  *
  */

public class getReserved1 {
	public static void main(String[] args){	
		Connection con;
		String driver = "com.mysql.jdbc.Driver";
		String url = "jdbc:mysql://abcdefg.mysql.db.hijklmno.com:12345/pqstuvwdb";
		String user = "username";
		String password = "password";
		List<String> list = new ArrayList<String>();
		try{
			Class.forName(driver);
			// getConnection()方法，连接MySQL数据库！！
			con = DriverManager.getConnection(url, user, password);
			if (!con.isClosed()){
				System.out.println("Succeeded connecting to the Database!");
			}
					
			String sql = "select reserved1 from voiceanarecresult_table where serviceName = 'Nt_bbmanager_Sbc' and reserved1 is not null and reserved2 = '8' order by id desc limit 20";
			PreparedStatement pst = null;
			
			try{
				pst = (PreparedStatement) con.prepareStatement(sql);
				ResultSet rs = pst.executeQuery();
				while(rs.next()){
					list.add(rs.getString("reserved1"));
				}
			}catch(Exception e){	
			}
			con.close();
			
			}catch (ClassNotFoundException e) {
				e.printStackTrace();
			} catch (SQLException e) {
				e.printStackTrace();
			} catch (Exception e) {
				e.printStackTrace();
			}
				
		for(int i = 1; i < list.size()-1; i ++ ){
			//System.out.println(list.get(i-1));
			saveAsTxt st = new saveAsTxt();
			st.saveReserved1(list.get(i-1),i);
		}
	}
}
