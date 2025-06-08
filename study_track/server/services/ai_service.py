from datetime import datetime
from openai import OpenAI
import json
from typing import Dict, Any



class AIService:
    def __init__(self):
        self.client = OpenAI(
            api_key="sk-6a355e33eb7c4021b82b0742a2c980d1",
            base_url="https://api.deepseek.com"
        )

    # ---------- 公共方法 ----------
    def _call_ai_api(self, messages: list, model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if response.usage else {}
            }
        except Exception as e:
            return {"error": str(e)}

    def _format_response(self, api_response: Dict[str, Any], is_json: bool = False) -> Dict[str, Any]:
        if "error" in api_response:
            return {
                "status": "error",
                "error": api_response["error"],
                "metadata": {"timestamp": datetime.now().isoformat()}
            }

        raw_content = api_response["content"]

        if is_json:
            # 清理 markdown 包裹（如 ```json ... ```）
            if raw_content.strip().startswith("```"):
                lines = raw_content.strip().splitlines()
                # 去掉第一行（```json）和最后一行（```），中间是纯 JSON 字符串
                raw_content = "\n".join(lines[1:-1])
            try:
                content = json.loads(raw_content)
            except json.JSONDecodeError:
                content = {"raw_text": raw_content, "warning": "无法解析为JSON，可能是格式问题"}
        else:
            content = raw_content

        return {
            "result": content,
            "metadata": {
                "model": "deepseek-chat" if is_json else "deepseek-reasoner",
                "token_usage": api_response.get("usage", {}),
                "timestamp": datetime.now().isoformat()
            },
            "status": "success"
        }

    # ---------- 学习建议 ----------
    def get_study_advice(self, academic_data: Dict[str, Any]) -> Dict[str, Any]:
        """完整处理流程"""
        # 参数校验
        if not academic_data.get('scores'):
            return {"error": "Missing required scores data"}

        # 生成对话prompt
        messages = self.generate_study_prompt(academic_data)

        # 调用AI接口
        api_response = self._call_ai_api(
            messages,
            model="deepseek-reasoner",
            temperature=0.5,
            max_tokens=1024
        )

        # 统一返回格式
        return {
            "advice": api_response.get("content"),
            "metadata": {
                "model": "deepseek-reasoner",
                "token_usage": api_response.get("usage", {}),
                "timestamp": datetime.now().isoformat()
            },
            "status": "success" if "content" in api_response else "error",
            "error": api_response.get("error")
        }

    def generate_study_prompt(self, academic_data: Dict[str, Any]) -> list:
        """生成对话prompt"""
        system_prompt = """你是一个专业的教育顾问，需要根据学生的专业信息和各科成绩，提供针对性的学习建议。请结合课程关联性和成绩分布进行分析。"""

        user_prompt = f"""
        学生信息：
        - 专业：{academic_data.get('major', '未知')}
        - 年级：{academic_data.get('grade', '未注明')}

        成绩数据：
        {json.dumps(academic_data.get('scores', {}), indent=2)}

        请根据以上信息，重点分析：
        1. 优势学科与待加强学科
        2. 专业核心课程的掌握情况
        3. 跨学科的知识衔接建议
        4. 学习资源推荐
        """

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    # ---------- 绩点预测 ----------
    def _generate_gpa_prompt(self, history_data: Dict[str, Any]) -> list:
        system_prompt = (
            "你是一个专业的学术预测模型，需要根据学生的历史成绩数据预测下一个学期的GPA，"
            "并基于过往的成绩变化趋势，提供一段分析GPA走势和学习建议的文案。"
            "请确保返回合法的JSON格式，包含字段：semester、gpa 和 trend_analysis。"
        )
        user_prompt = f"""基于以下历史数据预测未来一个学期的GPA，并提供趋势分析：
        {json.dumps(history_data, indent=2, ensure_ascii=False)}
        返回格式示例：
        {{
            "semester": "2025春",
            "gpa": 3.8,
            "trend_analysis": "整体成绩表现稳定，核心课程提升明显，GPA呈上升趋势，建议保持复习频率。"
        }}"""
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    def predict_gpa(self, history_data: Dict[str, Any]) -> Dict[str, Any]:
        if not history_data.get("semester_gpa"):
            return {"error": "缺少历史绩点数据"}

        messages = self._generate_gpa_prompt(history_data)
        api_response = self._call_ai_api(
            messages,
            model="deepseek-chat",
            temperature=0.3,
            max_tokens=400
        )
        if "error" in api_response:
            return {
                "status": "error",
                "error": api_response["error"],
                "metadata": {"timestamp": datetime.now().isoformat()}
            }

        return self._format_response(api_response, is_json=True)
