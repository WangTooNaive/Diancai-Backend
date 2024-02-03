from openai import OpenAI
from pathlib import Path
import httpx
import configparser

app_path = Path(__file__).resolve().parent.parent  # 项目根目录（`/app`）

class TxtConverter:
    def __init__(self):
        self.api_key = self.load_api_key()

    def load_api_key(self):
        config = configparser.ConfigParser()
        config_file = app_path / 'api_key.ini'
        config.read(config_file)

        api_key = config['OpenAI'].get('API_KEY')

        if not api_key:
            # 如果没有找到API密钥，可以要求用户手动输入或引发异常
            api_key = input("Enter your OpenAI API key: ")

            # 将新的API密钥保存到配置文件中
            config['OpenAI']['API_KEY'] = api_key
            with open(config_file, 'w') as configfile:
                config.write(configfile)

        return api_key

    def txt_converter(self, content):
        client = OpenAI(
            base_url="https://oneapi.xty.app/v1",
            api_key=self.api_key,
            http_client=httpx.Client(
                base_url="https://oneapi.xty.app/v1",
                follow_redirects=True,
            ),
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Convert in less than 200 characters this image caption to a very concise musical description with musical terms, as if you wanted to describe a musical ambiance, stricly in English"},
                {"role": "user", "content": content}
            ]
        )
        converted_result = completion.choices[0].message.content
        print("converted result:" + converted_result.encode('gbk', errors='replace').decode('gbk'))
        return converted_result

if __name__ == "__main__":
    content = "the image shows a bright star in the center of a galaxy"
    txt_con = TxtConverter()
    converted_result = txt_con.txt_converter(content)
    # print(converted_result)