import pytest
from similarity_v1 import assess_answer


# arr= [("This is a sample test case","This is a sample test case"), ("The world is a beautiful place","Cars are the best")]
small_correct= []
small_error= []
long_correct = []
long_error = []

file1 = open('small_correct.txt', 'r')
file2 = open('small_wrong.txt', 'r')
file3 = open('long_correct.txt', 'r')
file4 = open('long_wrong.txt', 'r')

Lines1 = file1.readlines()
Lines2 = file2.readlines()
Lines3 = file3.readlines()
Lines4 = file4.readlines()

for line in Lines1:
    line = line.strip()
    a,b = line.split(';')
    small_correct.append((a,b))

for line in Lines2:
    line = line.strip()
    a,b = line.split(';')
    small_error.append((a,b))

for line in Lines3:
    line = line.strip()
    a,b = line.split(';')
    long_correct.append((a,b))


for line in Lines4:
    line = line.strip()
    a,b = line.split(';')
    long_error.append((a,b))



# @pytest.mark.parametrize("a,b", small_correct)
# def test_small_correct(a,b):
#     assert assess_answer(a,b,5) == 5

# @pytest.mark.parametrize("a,b", long_correct)
# def test_large_correct(a,b):
#     assert assess_answer(a,b,10) == 10

# @pytest.mark.parametrize("a,b", small_error)
# def test_small_correct(a,b):
#     val = assess_answer(a,b,5)
#     val = 5 -val
#     assert val >= 1

# @pytest.mark.parametrize("a,b", long_error)
# def test_large_correct(a,b):
#     val = assess_answer(a,b,10)
#     val = 10 -val
#     assert val >= 2
