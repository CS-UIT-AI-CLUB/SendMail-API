import smtplib, ssl
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tqdm import tqdm
from threading import Thread


class EmailThread(Thread):
    def __init__(self, user_name, password, title, contacts_list, template):
        self.user_name = user_name
        self.password = password
        self.title = title
        self.contacts_list = contacts_list
        self.template = template
        Thread.__init__(self)


    def run (self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.user_name, self.password)
                
            for contact in self.contacts_list:
                message = MIMEMultipart("alternative")
                message["Subject"] = self.title
                message["From"] = self.user_name
                message["To"] = contact['email']
                
                html = self.template.format(**contact)
                message.attach(MIMEText(html, "html"))
                
                server.sendmail(
                    self.user_name,
                    contact['email'],
                    message.as_string(),
                )
                
def get_contacts_list(fi):
    df = pd.read_csv(fi)
    
    df['num_member'] = df.apply(lambda row: pd.notnull(row['id1']) + pd.notnull(row['id2']) + pd.notnull(row['id3']), axis=1)
    df['member1'] = df.apply(lambda row: '' if pd.isnull(row['name1']) else 
                                '<li>Thành viên thứ nhất: <b>{}</b>. Mã số sinh viên: <b>{:.0f}</b>.</li>'.format(row['name1'], row['id1']), axis=1)
    df['member2'] = df.apply(lambda row: '' if pd.isnull(row['name2']) else 
                                '<li>Thành viên thứ hai: <b>{}</b>. Mã số sinh viên: <b>{:.0f}</b>.</li>'.format(row['name2'], row['id2']), axis=1)
    df['member3'] = df.apply(lambda row: '' if pd.isnull(row['name3']) else 
                                '<li>Thành viên thứ ba: <b>{}</b>. Mã số sinh viên: <b>{:.0f}</b>.</li>'.format(row['name3'], row['id3']), axis=1)
    
    contacts_list = df.to_dict('records')
    return contacts_list
                
# if __name__ == "__main__":
#     username = "aiclub.cs.uit@gmail.com"
#     password = "aiclubcsuit^@%"
#     title = "[AI Tempo Run] Thông báo nộp bài cho giai đoạn private test"
    
#     contacts_list = get_contacts_list('team_list_final.csv')
    
#     template = ''' \
#         <html> <body> <font size="4">
#             <p> Thân chào đội thi <b>{team_name}</b>, </p>
            
#             <p> Cuộc đua AI Tempo Run hiện vẫn diễn ra vô cùng gay cấn với giai đoạn public test đang dần đến hồi kết. \
#                 Ban tổ chức cuộc thi gửi email đến đội <b>{team_name}</b> thông báo rằng đã đến thời gian nộp bài cho vòng private test. </p>
                
#             <p> Trước hết, chúng tôi xin được phép xác nhận thông tin của đội thi <b>{team_name}</b> gồm có \
#                 0{num_member} thành viên:
                
#             <ul>
#                 {member1}
#                 {member2}
#                 {member3}
#             </ul>
            
#             </p>    
            
#             <p> Để tiến hành nộp bài cho giai đoạn private test, xin vui lòng phản hồi phía dưới email này. \
#                 Bài nộp có thể được đính kèm dưới dạng tệp tin <b>.ipynb</b> hoặc tệp tin <b>.zip</b> chứa bài làm của đội. \
#                 Các đội có thể sử dụng chức năng xuất tệp tin <b>.ipynb</b> của Google Colab hoặc Kaggle rồi tải về máy tính để nộp. </p>
                
#             <p> Nhằm đảm bảo tính công bằng cho cuộc thi, bên cạnh lời giải thì các đội cần cung cấp cả source code dùng để \
#                 <b>huấn luyện mô hình</b>. Ban tổ chức sẽ thực hiện huấn luyện lại mô hình để xác định kết quả cuối cùng. </p>
                
#             <p> Những đội thi có lời giải hay, được chú thích (comment) rõ ràng và mô tả ngắn gọn về ý tưởng của mình \
#                 sẽ được xem xét trao giải <b><i>"Ý tưởng sáng tạo"</b></i>, đồng thời lời giải của đội sẽ được chia sẻ lên fanpage \
#                 <b>Câu lạc bộ AI - Khoa Khoa học Máy tính</b> để các sinh viên khác tham khảo và học hỏi. </p>
                
#             <p> Các đội vui lòng phản hồi email này trước <b>17h00 thứ Sáu ngày 21/05/2021</b>. Ban tổ chức không chấp nhận bất kỳ \
#                 khiếu nại nào nếu các đội phản hồi trễ hoặc bài nộp không thực thi đúng cách. </p>
                
#             <p> Trân trọng. </p>
            
#             </font>
#             <table>
#                 <tr>
#                     <td><img width="96" height="96" src="https://i.imgur.com/ZpmwfQF.png"></td>
#                     <td> <p> 
#                         &nbsp;&nbsp; <font size="4"> <b> Câu lạc bộ AI - Khoa Khoa học Máy tính </b> </font> <br>
#                         &nbsp;&nbsp; <b> <i> Đại học Công nghệ Thông tin - ĐHQG TP.HCM </i> </b> <br>
#                         &nbsp;&nbsp; <a href="mailto:aiclub.cs.uit@gmail.com"> aiclub.cs.uit@gmail.com </a> <br>
#                         &nbsp;&nbsp; <a href="http://tutorials.aiclub.cs.uit.edu.vn"> AI CLUB Tutorials </a> <br>
#                     </p> </td>
#                 </tr>
#             </table>

            
#         </body> </html>
#     '''
    
#     thread1 = EmailThread(username, password, title, contacts_list, template)
#     thread1.start()