import Translation.brl_to_txt as b2t
import ContextualErrorCorrection.contextual_error_correction as cec
import Translation.txt_to_brl as t2b
import FeedbackGeneration.feedback_generator as fg
import json

print("Validation started.")

print("Validation of Translation/brl_to_txt.py")
b2t.test()
print("Validation of ContextualErrorCorrection/contextual_error_correction.py")
cec.test()
print("Validation of Translation/txt_to_brl.py")
t2b.test()
print("Validation of FeedbackGeneration/feedback_generator.py")
fg.test()
        