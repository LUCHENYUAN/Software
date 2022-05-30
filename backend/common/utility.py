import random, string
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw


class ImageCode:
    def gen_text(self):
        # sample用于从一个大的列表或字符串随机取得n个字符
        list = random.sample(string.ascii_letters + string.digits, 4)
        return ''.join(list)

    def rand_color(self):
        red = random.randint(32, 127)
        green = random.randint(32, 127)
        blue = random.randint(32, 127)
        return red, green, blue

    def draw_verify_code(self):
        code = self.gen_text()
        width, height = 120, 50

        im = Image.new('RGB', (width, height), 'white')

        font = ImageFont.truetype(font='arial.ttf', size=40)
        draw = ImageDraw.Draw(im)

        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)

        # 绘制干扰线
        self.draw_lines(draw, 3, width, height)
        # im.show()
        return im, code

    def draw_lines(self, draw, n, width, height):
        for num in range(n):
            x1 = random.randint(0, width / 2)
            x2 = random.randint(0, width)
            y1 = random.randint(0, height / 2)
            y2 = random.randint(0, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=2)

    # 生成图片验证码并返回给控制器
    def get_code(self):
        image, code = self.draw_verify_code()
        buf=BytesIO()
        image.save(buf,format='jpeg')
        bstr=buf.getvalue() #二进制码
        return code,bstr

#邮件相关操作
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

def send_email(receiver,ecode):
    sender='Foods&Sports<1193458126@qq.com>'

    content=f"<br/>欢迎使用Letscode，<span style='color:red;font-size:20px;'>{ecode}</span>"\
    "请尽快去主页查看详情"
    #实例化邮件对象，并制定关键参数
    message=MIMEText(content,'html','utf-8')
    #指定邮件的标题
    message['Subkect']=Header('Foods&Sports-注册验证码','utf-8')
    message['From']=sender
    message['To']=receiver

    smtpOBJ=SMTP_SSL('smtp.qq.com')
    smtpOBJ.login(user='1193458126@qq.com',password='ezdzogxsrkayjcja')
    smtpOBJ.sendmail(sender,receiver,str(message))
    smtpOBJ.quit()

def gen_email_code():
    str=random.sample(string.ascii_letters+string.digits,6)
    return ''.join(str)

#单个模型类转化为标准json
def model_list(result):
    list = []
    for obj1, obj2 in result:
        dict = {}
        for k1, v1 in obj1.__dict__.items():
            if not k1.startswith('_sa_instance_state'):
                dict[k1] = v1

        list.append(dict)
    return list

#SQLAlchemy连接查询2张表转换为JSON[{},{},...]
def model_join_list(result):
    list=[]
    for obj1,obj2 in result:
        dict={}
        for k1,v1 in obj1.__dict__.items():
            if not k1.startswith('_sa_instance_state'):
                dict[k1]=v1
        for k2,v2 in obj1.__dict__.items():
            if not k2.startswith('_sa_instance_state'):
                if not k2 in dict:
                    dict[k2]=v2
        list.append(dict)
    return list


if __name__=='__main__':
    str='洛谷,LeetCode力扣,牛客网,AtCoder,CodeForces'
    print(len(str))


