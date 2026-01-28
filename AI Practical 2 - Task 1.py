from experta import *

class Gesture(Fact):
    mood = Field(str)
    answer = Field(str)

class FacialGestureAgent(KnowledgeEngine):

    @Rule(Gesture(mood="happy", answer="positive"))
    @Rule(Gesture(mood="happy", answer="unsure"))
    def happy_smile(self):
        print("Perform smiling gesture")

    @Rule(Gesture(mood="happy", answer="negative"))
    def happy_nod(self):
        print("Perform nodding gesture")

    @Rule(Gesture(mood="sad"))
    def sad_frown(self):
        print("Perform frowning gesture")

    @Rule(Gesture(mood="neutral", answer="positive"))
    @Rule(Gesture(mood="neutral", answer="negative"))
    def neutral_nod(self):
        print("Perform nodding gesture")

    @Rule(Gesture(mood="neutral", answer="unsure"))
    def neutral_blink(self):
        print("Perform blinking gesture")


mood, answer = input("Enter input as tuple (mood, answer): ").strip("()").replace(" ", "").split(",")

engine = FacialGestureAgent()
engine.reset()
engine.declare(Gesture(mood=mood, answer=answer))
engine.run()
