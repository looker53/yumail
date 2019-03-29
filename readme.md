
## Quick Start
```python
from yumail import Mail


mail = Mail('example@163.com', 'pwd')
msg = "hello."
mail.send_mail('example@163.com', msg, subject="test")
```