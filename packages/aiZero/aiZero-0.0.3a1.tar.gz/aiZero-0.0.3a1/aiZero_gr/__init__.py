import os
from flask import Flask, render_template, jsonify, request, url_for, send_from_directory
import base64
import threading
from pathlib import Path
import uuid
import logging
from http import HTTPStatus
import dashscope
import requests
import time
import json


RESOURCE_PATH = Path(__file__).parent.resolve()


def resolve_resource_path(path):
    """
    解析资源路径：将相对路径与应用的资源路径结合，返回绝对路径。

    参数:
    path (str): 相对资源路径。

    返回:
    Path: 绝对资源路径。
    """
    return Path(RESOURCE_PATH / path).resolve()


# 大模型文字交互
def text_generation(chat_history, prompt='你是一个人工智能助手，你的名字叫小H', stream=False):
    """
    与大模型进行文字交互，基于给定的对话历史和提示进行响应生成。

    参数:
    chat_history (list): 对话历史，每个元素为用户或助手的一条消息。
    prompt (str): 提示文本，用于引导模型的响应，默认为"你是一个人工智能助手，你的名字叫小H"。
    stream (bool): 是否以流式方式获取生成结果，默认为False。

    返回:
    str: 模型生成的响应文本，或错误信息。
    """
    def generator():
        # 生成器，用于流式返回响应
        for r in response:
            if r.status_code == HTTPStatus.OK:
                yield r.output.choices[0]['message']['content']
            else:
                return "错误: " + r.message

    try:
        result = words_check(chat_history[-1])
        if result['status'] == 'error':
            return result['message']
        result = words_check(prompt)
        if result['status'] == 'error':
            return result['message']

        messages = [{'role': 'system', 'content': prompt}]
        for index, content in enumerate(chat_history):
            if len(content) != 0:
                if index % 2 == 0:
                    messages.append({'role': 'user', 'content': content})
                else:
                    messages.append({'role': 'assistant', 'content': content})
            else:
                return '输入参数错误'

        response = dashscope.Generation.call(model="qwen-plus",
                                             messages=messages,
                                             result_format='message',
                                             stream=stream)
        if stream:
            return generator()
        else:
            if response.status_code == HTTPStatus.OK:
                return response.output.choices[0]['message']['content']
            else:
                return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)


# 大模型图像理解
def image_understanding(img, chat_history, prompt='你是一名人工智能助手', stream=False):
    """
    大模型对图像进行理解，基于对话历史和图像进行响应生成。

    参数:
    img (str): 图像的本地路径或URL。
    chat_history (list): 对话历史，每个元素为用户或助手的一条消息。
    prompt (str): 提示文本，用于引导模型的响应，默认为"你是一名人工智能助手"。
    stream (bool): 是否以流式方式获取生成结果，默认为False。

    返回:
    str: 模型生成的响应文本，或错误信息。
    """
    def generator():
        # 生成器，用于流式返回响应
        for r in response:
            if r.status_code == HTTPStatus.OK:
                yield r.output.choices[0].message.content[0]['text']
            else:
                return "错误: " + r.message

    try:
        result = words_check(chat_history[-1])
        if result['status'] == 'error':
            return result['message']
        result = words_check(prompt)
        if result['status'] == 'error':
            return result['message']

        img_url = upload_file(img)
        messages = [{'role': 'system', 'content': [{'text': prompt}]},
                    {'role': 'user', 'content': [{'image': img_url}, {'text': chat_history[0]}]}]

        for index, content in enumerate(chat_history[1:]):
            if index % 2 == 0:
                messages.append({'role': 'assistant', 'content': [{'text': content}]})
            else:
                messages.append({'role': 'user', 'content': [{'text': content}]})

        response = dashscope.MultiModalConversation.call(model='qwen-vl-plus',
                                                         messages=messages,
                                                         stream=stream)
        if stream:
            return generator()
        else:
            if response.status_code == HTTPStatus.OK:
                return response.output.choices[0].message.content[0]['text']
            else:
                return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)


# 大模型声音理解
def audio_understanding(audio, chat_history, prompt='你是一名人工智能助手', stream=False):
    """
    大模型对声音进行理解，基于对话历史和音频进行响应生成。

    参数:
    audio (str): 音频的本地路径或URL。
    chat_history (list): 对话历史，每个元素为用户或助手的一条消息。
    prompt (str): 提示文本，用于引导模型的响应，默认为"你是一名人工智能助手"。
    stream (bool): 是否以流式方式获取生成结果，默认为False。

    返回:
    str: 模型生成的响应文本，或错误信息。
    """
    def generator():
        # 生成器，用于流式返回响应
        for r in response:
            if r.status_code == HTTPStatus.OK:
                yield r.output.choices[0].message.content[0]['text']
            else:
                return "错误: " + r.message

    try:
        result = words_check(chat_history[-1])
        if result['status'] == 'error':
            return result['message']
        result = words_check(prompt)
        if result['status'] == 'error':
            return result['message']

        audio_url = upload_file(audio)
        messages = [{'role': 'system', 'content': [{'text': prompt}]},
                    {'role': 'user', 'content': [{'audio': audio_url}, {'text': chat_history[0]}]}]
        for index, content in enumerate(chat_history[1:]):
            if index % 2 == 0:
                messages.append({'role': 'assistant', 'content': [{'text': content}]})
            else:
                messages.append({'role': 'user', 'content': [{'text': content}]})

        response = dashscope.MultiModalConversation.call(model='qwen-audio-turbo',
                                                         messages=messages,
                                                         stream=stream)
        if stream:
            return generator()
        else:
            if response.status_code == HTTPStatus.OK:
                return response.output.choices[0].message.content[0]['text']
            else:
                return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)


# 大模型图像生成
def image_generation(prompt):
    """
    根据提示文本生成图像。

    参数:
    prompt (str): 提示文本，用于指导图像生成。

    返回:
    str: 生成的图像URL，或错误信息。
    """
    try:
        result = words_check(prompt)
        if result['status'] == 'error':
            return result['message']

        response = dashscope.ImageSynthesis.async_call(model='wanx-v1',
                                                       prompt=prompt,
                                                       n=1,
                                                       size='1024*1024')
        if response.status_code == HTTPStatus.OK:
            rsp = dashscope.ImageSynthesis.wait(response)
            if rsp.status_code == HTTPStatus.OK:
                return rsp.output.results[0].url
            else:
                return "错误: " + response.message
        else:
            return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)



# 大模型人像风格重绘
def human_repaint(img, style=7):
    """
    使用大模型对人像图片进行风格重绘。

    参数:
    img: 图像文件，本地路径或网络URL。
    style: 风格指数，默认为7。

    返回值:
    重绘后的图像URL或错误信息。
    """
    try:
        img_url = upload_file(img)  # 上传图像文件
        url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': dashscope.api_key,
            'X-DashScope-Async': 'enable'
        }

        params = {
            'model': 'wanx-style-repaint-v1',
            'input': {
                'image_url': img_url,
                'style_index': style
            }
        }

        response = requests.post(url, headers=headers, json=params)
        if response.status_code == 200:
            task_id = response.json()['output']['task_id']
            # 异步任务，轮询任务状态直到完成或失败
            while True:
                time.sleep(3)
                response = requests.get('https://dashscope.aliyuncs.com/api/v1/tasks/{}'.format(task_id),
                                        headers={'Authorization': dashscope.api_key})
                if response.status_code == 200:
                    if response.json()['output']['task_status'] == 'SUCCEEDED':
                        return response.json()['output']['results'][0]['url']
                    elif response.json()['output']['task_status'] == 'FAILED':
                        return "错误: " + response.json()['output']['message']
                else:
                    return "错误: " + response.json()['message']
        else:
            return "错误: " + response.json()['message']
    except Exception as e:
        return "错误: " + str(e)


# 涂鸦作画
def sketch_to_image(img, prompt, style='<anime>'):
    """
    将涂鸦图像转换为现实图像。

    参数:
    img: 涂鸦图像文件，本地路径或网络URL。
    prompt: 描述期望图像的文字提示。
    style: 风格标签，默认为'<anime>'。

    返回值:
    生成的图像URL或错误信息。
    """
    try:
        result = words_check(prompt)  # 检查文字提示是否合规
        if result['status'] == 'error':
            return result['message']
        img_url = upload_file(img)  # 上传图像文件
        url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': dashscope.api_key,
            'X-DashScope-Async': 'enable'
        }

        params = {
            'model': 'wanx-sketch-to-image-lite',
            'input': {
                'sketch_image_url': img_url,
                'prompt': prompt
            },
            'parameters': {
                'size': '768*768',
                'n': 1,
                'style': style
            }
        }

        response = requests.post(url, headers=headers, json=params)
        if response.status_code == 200:
            task_id = response.json()['output']['task_id']
            # 异步任务，轮询任务状态直到完成或失败
            while True:
                time.sleep(3)
                response = requests.get('https://dashscope.aliyuncs.com/api/v1/tasks/{}'.format(task_id),
                                        headers={'Authorization': dashscope.api_key})
                if response.status_code == 200:
                    if response.json()['output']['task_status'] == 'SUCCEEDED':
                        return response.json()['output']['results'][0]['url']
                    elif response.json()['output']['task_status'] == 'FAILED':
                        return "错误: " + response.json()['output']['message']
                else:
                    return "错误: " + response.json()['message']
        else:
            return "错误: " + response.json()['message']
    except Exception as e:
        return "错误: " + str(e)


# 语音识别
def speech_recognition(audio):
    """
    将语音转换为文字。

    参数:
    audio: 语音文件，本地路径或网络URL。

    返回值:
    识别出的文字或错误信息。
    """
    try:
        audio_url = upload_file(audio)  # 上传语音文件
        task_response = dashscope.audio.asr.Transcription.async_call(
            model='paraformer-v1',
            file_urls=[audio_url]
        )
        transcribe_response = dashscope.audio.asr.Transcription.wait(task=task_response.output.task_id)
        if transcribe_response.status_code == HTTPStatus.OK:
            result = transcribe_response.output
            if result['task_status'] == 'SUCCEEDED':
                json_url = result['results'][0]['transcription_url']
                response = requests.get(json_url)
                if response.status_code == 200:
                    data = response.json()
                    return data['transcripts'][0]['text']
                else:
                    return '错误: 结果获取出错'
            else:
                return '错误: 解码错误'
        else:
            return '错误: 解析错误'
    except Exception as e:
        return "错误: " + str(e)


# 语音合成
def speech_synthesis(text, model='sambert-zhiying-v1', rate=1, pitch=1):
    """
    将文字转换为语音。

    参数:
    text: 要合成的文字。
    model: 合成语音的模型，默认为'sambert-zhiying-v1'。
    rate: 语速调整，默认为1。
    pitch: 语调调整，默认为1。

    返回值:
    合成的语音文件路径或错误信息。
    """
    try:
        result = dashscope.audio.tts.SpeechSynthesizer.call(model=model,
                                                            text=text,
                                                            rate=rate,  # 0.5-2
                                                            pitch=pitch)  # 0.5-2
        if result.get_audio_data() is not None:
            audio_data = result.get_audio_data()
            filename = f"{uuid.uuid4()}.wav"
            output_file_path = str(resolve_resource_path(f'static/audios/{filename}'))
            with open(output_file_path, 'wb') as audio_file:
                audio_file.write(audio_data)
            return f'static/audios/{filename}'
        else:
            return '错误: ' + result.get_response().message
    except Exception as e:
        return "错误: " + str(e)


def upload_file(file_path):
    """
    上传文件到服务器。

    参数:
    file_path: 文件路径，本地路径或网络URL。

    返回值:
    上传后的文件URL或错误信息。
    """
    file_path = str(resolve_resource_path(file_path))
    if not os.path.exists(file_path):
        return file_path
    with open(file_path, 'rb') as file:
        files = {'file': (file_path, file)}
        response = requests.post('https://fileserver.hlqeai.cn/upload', files=files)
    if response.status_code == 201:
        print("文件上传成功")
        print(response.json()['url'])
        return response.json()['url']
    else:
        print(response.status_code, response.text)
        raise Exception(
            'Error Message: {}, Status Code: {}, Response: {}'.format('文件上传失败', response.status_code, response.text))


def words_check(content):
    """
    检查文本中是否含有违禁词。

    参数:
    content: 要检查的文本。

    返回值:
    检查结果，包含状态和消息。
    """
    url = "http://wordscheck.hlqeai.cn/wordscheck"
    data = json.dumps({'content': content})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    if response.json()['code'] == '0':
        if response.json()['word_list']:
            return {'status': 'error', 'message': '您的输入信息可能含有违禁词，请谨慎输入'}
        else:
            return {'status': 'success', 'message': ''}
    else:
        return {'status': 'error', 'message': response.json()['msg']}



import gradio as gr

class AIWebApp:
    """
    一个基于Flask框架的人工智能Web应用程序类。
    """

    def __init__(self, title='My AI Web App'):
        pass

    def set_apikey(self, key):
        """
        设置API密钥。

        :param key: API密钥。
        """
        dashscope.api_key = key

    def add_input_text(self):
        """
        添加文本输入组件到组件列表。
        """
        self.components.append({
            'type': 'input_text',
            'id': 'textComponent'
        })

    def add_camera(self):
        """
        添加摄像头组件到组件列表。
        """
        self.components.append({
            'type': 'camera',
            'id': 'cameraComponent'
        })

    def add_record(self):
        """
        添加录音组件到组件列表。
        """
        self.components.append({
            'type': 'record',
            'id': 'recordComponent'
        })

    def add_pic_file(self):
        """
        添加图片上传组件到组件列表。
        """
        self.components.append({
            'type': 'input_pic',
            'id': 'inputPicComponent'
        })

    def add_audio_file(self):
        """
        添加音频上传组件到组件列表。
        """
        self.components.append({
            'type': 'input_audio',
            'id': 'inputAudioComponent'
        })

    def add_submit(self, callback=None):
        """
        添加提交按钮组件到组件列表，并设置提交时的回调函数。

        :param callback: 提交时的回调函数。
        """
        self.ai_callback = callback

    def run(self, **kwargs):
        demo = gr.ChatInterface(fn=self.ai_callback, multimodal=True)
        demo.launch()
