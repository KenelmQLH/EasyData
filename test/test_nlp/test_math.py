from EasyData.NLPHandler.Math import infix_to_postfix

exp1 = list("(((1+2)*3)+1)")
exp2 = list("(1+2)*3+1-2")

pos1 = infix_to_postfix(exp1)
print(pos1)

pos2 = infix_to_postfix(exp2)
print(pos2)