# PROVE IT — Day 01: Find the Problem

مهمة Day 01 من مسابقة PROVE IT (Arabian Academy — AI Engineering Track): اكتشاف وإصلاح Bug مخفي في كود Python بسيط لـ AI Pipeline.

## الكود الأصلي (`before`)

كلاس `SimpleAIPipeline` بيستقبل prompt من المستخدم، يتأكد من طوله، ويسجّله في `history`، وفيه دالة `get_average_prompt_length()` بتحسب متوسط أطوال الـprompts السابقة.

## الـBug

`get_average_prompt_length()` بتقسم `total_length` على `len(self.history)` من غير ما تتأكد إن فيه بيانات أصلًا:

```python
def get_average_prompt_length(self):
    total_length = sum([len(item["echo"]) for item in self.history])
    return total_length / len(self.history)
```

لو الدالة اتنادى قبل أي `process_input()`، `self.history` بتبقى `[]`، يبقى `len(self.history) = 0`، ويحصل:

```
ZeroDivisionError: division by zero
```

**الإثبات:** اتشغّل الكود فعليًا — إنشاء `SimpleAIPipeline` جديدة، ونداء مباشر على `get_average_prompt_length()` من غير أي prompt قبلها، والكود كرش فورًا بنفس الـError.

**ليه مهم في الإنتاج:** أي جزء تاني في السيستم (زي dashboard أو monitoring tool) ممكن ينادي على الدالة دي قبل ما أول request يوصل، فالسيرفس كله يقع من أول ثانية.

## الحل (`after`)

```python
def get_average_prompt_length(self):
    if not self.history:
        return 0.0
    total_length = sum(len(item["echo"]) for item in self.history)
    return total_length / len(self.history)
```

guard clause بيتحقق لو الـhistory فاضية قبل القسمة، ويرجّع `0.0` بدل الكراش — ده بيعالج سبب المشكلة (غياب الـvalidation)، مش مجرد `try/except` بيغطي الـException بعد حدوثها.

## تحسينات إضافية اتعملت في `after`

| التحسين | ليه |
|---|---|
| تأكيد إن الـinput أصلًا `string` | كان بيكرش بـ `AttributeError` مع `None` |
| تقدير Tokens حقيقي بدل عدّ Characters | `max_tokens` كان بيقيس حروف مش Tokens فعلية |
| `deque(maxlen=...)` بدل `list` عادية | يمنع Memory Leak من history بتكبر من غير حد |
| كل الأخطاء بترجع dict `{"status": "error", ...}` | يوحّد شكل الأخطاء مع شكل النجاح، بدل `raise` غير متسق |
| شيل `import json` غير المستخدم + `sum()` بقت generator | تنظيف الكود وتوفير ميموري |

## الملفات

| الملف | الوصف |
|---|---|
| `simple_ai_pipeline_before.py` / `.ipynb` | الكود الأصلي زي ما هو في المهمة |
| `simple_ai_pipeline_after.py` / `.ipynb` | الكود بعد كل التعديلات، وكل تعديل معلّق عليه بالـليه |
