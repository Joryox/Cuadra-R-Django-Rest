import os

path = r"c:\Users\jorge\OneDrive\Escritorio\Cuadra Erre\Cuadra\Cuadra-R-Django-Rest\api\views.py"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "if check_password(password, user.password):" in line:
        new_lines.append(line)
        new_lines.append("            from rest_framework.authtoken.models import Token\n")
        new_lines.append("            token, _ = Token.objects.get_or_create(user=user)\n")
        new_lines.append("            return Response({\n")
        new_lines.append("                \"message\": \"Login exitoso\",\n")
        new_lines.append("                \"token\": token.key,\n")
        skip = True
    elif skip and "\"token\": token," in line:
        skip = False
        continue
    elif skip:
        continue
    else:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
