# import lazyllm
#
# chat = lazyllm.OnlineChatModule(source='glm', model='GLM-4.5')
# while True:
#     query = input("query(enter 'quit' to exit): ")
#     if query == "quit":
#         break
#     res = chat.forward(query)
#     print(f"answer: {res}")


import lazyllm
import re
from collections import defaultdict

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.log_data = defaultdict(list)
        self.log_levels = ["ERROR", "WARNING", "INFO"]

    def parse_logs(self):
        """解析日志文件，并按级别分类日志"""
        with open(self.log_file, 'r') as file:
            for line in file:
                for level in self.log_levels:
                    if level in line:
                        self.log_data[level].append(line.strip())
                        break

    def generate_summary(self):
        """生成日志的基本统计信息"""
        summary = {}
        for level in self.log_levels:
            summary[level] = len(self.log_data[level])
        return summary

    def get_log_details(self, level):
        """获取特定日志级别的详细信息"""
        return "\n".join(self.log_data[level])


class LogAnalysisAssistant:
    def __init__(self, log_file, chat_model='glm'):
        self.log_analyzer = LogAnalyzer(log_file)
        self.chat = lazyllm.OnlineChatModule(source='glm', model=chat_model)
        self.log_analyzer.parse_logs()

    def query_logs(self, query):
        """根据用户的查询生成答案"""
        summary = self.log_analyzer.generate_summary()
        if "ERROR" in query:
            return f"Total ERROR logs: {summary['ERROR']}\nDetails:\n{self.log_analyzer.get_log_details('ERROR')}"
        elif "WARNING" in query:
            return f"Total WARNING logs: {summary['WARNING']}\nDetails:\n{self.log_analyzer.get_log_details('WARNING')}"
        elif "INFO" in query:
            return f"Total INFO logs: {summary['INFO']}\nDetails:\n{self.log_analyzer.get_log_details('INFO')}"
        elif "summary" in query:
            return f"Log Summary: {summary}"
        else:
            return "I'm sorry, I didn't quite understand your query."

    def start(self):
        """启动查询助手，处理用户输入"""
        while True:
            query = input("query (enter 'quit' to exit): ")
            if query.lower() == "quit":
                break
            # 向 LLM 发送查询并获取结果
            res = self.chat.forward(self.query_logs(query))
            print(f"answer: {res}")

# 使用方法
log_file_path = "logfile.log"  # 替换为你的日志文件路径
assistant = LogAnalysisAssistant(log_file_path, chat_model='GLM-4.5')
assistant.start()

