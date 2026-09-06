from collections import deque
# تعديل: import json اتشالت لأنها كانت مستوردة من غير أي استخدام في الكود

class SimpleAIPipeline:
    def __init__(self, max_tokens=100, max_history=1000):
        self.max_tokens = max_tokens
        # تعديل: history بقت deque(maxlen=...) بدل list عادية
        # ليه: list عادية بتكبر من غير حد أقصى، وده Memory Leak لو
        # الـpipeline شغالة لفترة طويلة في الإنتاج. deque بترمي أقدم
        # عنصر لوحدها أول ما توصل للحد.
        self.history = deque(maxlen=max_history)

    @staticmethod
    def _estimate_tokens(text):
        # إضافة: تقدير Tokens حقيقي بدل عدّ Characters
        # ليه: اسم max_tokens كان بيوهم إنه بيقيس Tokens، بس الكود
        # القديم كان بيعدّ الحروف بس. هنا تقريب شائع من غير مكتبة
        # خارجية: كل ~4 حروف = Token واحد تقريبًا.
        return max(1, len(text) // 4)

    def process_input(self, user_prompt):
        # تعديل: تأكيد إن الـinput أصلًا string قبل .strip()
        # ليه: لو اتبعت None أو أي نوع تاني، الكود القديم كان بيكرش
        # بـ AttributeError. دلوقتي بيرجع error dict بدل الكراش.
        if not isinstance(user_prompt, str):
            return {"status": "error", "message": "user_prompt must be a string"}

        # Step 1: Simple prompt cleaning
        cleaned_prompt = user_prompt.strip()

        # تعديل: الحد بيتحسب بالـTokens المقدّرة بدل عدد الـCharacters
        # تعديل: بترجع error dict بدل ما تعمل raise لـValueError
        # ليه: عشان شكل الأخطاء يبقى متسق مع شكل النجاح
        # ({"status": "success"/"error", ...}) بدل ما يبقى فيه raise
        # في حالة وreturn عادي في حالة تانية
        if self._estimate_tokens(cleaned_prompt) > self.max_tokens:
            return {"status": "error", "message": "Prompt exceeds maximum token limit!"}

        # Step 3: Store the query in the pipeline's temporary memory
        response_data = {"status": "success", "echo": cleaned_prompt}
        self.history.append(response_data)
        return response_data

    def get_average_prompt_length(self):
        # تعديل (الـBug الأساسي في مهمة Day 01): guard clause لو الـhistory فاضية
        # ليه: الكود القديم كان بيقسم على len(self.history) وهو صفر،
        # فبيحصل ZeroDivisionError: division by zero. اتثبتت المشكلة دي
        # فعليًا بتشغيل الكود ونادّينا على الدالة قبل أي process_input().
        if not self.history:
            return 0.0

        # تعديل: sum() بقت generator expression (من غير [])
        # ليه: أخف على الميموري مع history كبيرة، مش لازم تتبني list كاملة الأول
        total_length = sum(len(item["echo"]) for item in self.history)
        return total_length / len(self.history)

# Test run
pipeline = SimpleAIPipeline(max_tokens=50)
print(pipeline.process_input("Hello AI, optimize this code."))

# دي كانت الحالة اللي بتكرش قبل التعديل (history فاضية قبل أي process_input)
fresh_pipeline = SimpleAIPipeline(max_tokens=50)
print(fresh_pipeline.get_average_prompt_length())  # بترجع 0.0 دلوقتي من غير كراش
