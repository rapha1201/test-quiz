import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# =======================================
# =========== CREATED BELOW =============
# =======================================

def test_question_with_invalid_points():
    with pytest.raises(Exception):
      question = Question(title='q1', points=-1)
    with pytest.raises(Exception):
      question = Question(title='q1', points=201)

def test_question_choice_removal():
  question = Question(title='q1')

  question.add_choice('choice one', False)
  question.add_choice('choice two', True)
  question.add_choice('choice three', False)

  question.remove_choice_by_id(2)

  assert len(question.choices) == 2
  assert question.choices[0].text == 'choice one'
  assert question.choices[1].text == 'choice three'

def test_question_remove_all_choices():
  question = Question(title='q1')

  question.add_choice('choice one', False)
  
  question.remove_all_choices()

  assert len(question.choices) == 0

  question.add_choice('choice one', False)
  question.add_choice('choice two', True)
  question.add_choice('choice three', False)

  question.remove_all_choices()

  assert len(question.choices) == 0

def test_question_choice_id():
  question = Question(title='q1')

  id1 = question.add_choice('c1', False).id
  id2 = question.add_choice('c2', False).id
  id3 = question.add_choice('c3', False).id

  question.remove_choice_by_id(id2)

  assert question.choices[1].id == id3

  id4 = question.add_choice('c4', True).id

  assert question.choices[2].id == id4

  question.remove_all_choices()

  id5 = question.add_choice('c1', False).id

  assert question.choices[0].id == id5

def test_question_remove_invalid_id():
  question = Question('q1')

  with pytest.raises(Exception):
    question.remove_choice_by_id(0)

  question.add_choice('c1', False)
  question.add_choice('c2', True)

  with pytest.raises(Exception):
    question.remove_choice_by_id(3)

def test_set_correct_choices():
  question = Question('q1')

  swap_to_true = []

  id_true_1 = question.add_choice('c1', False).id
  swap_to_true.append(id_true_1)

  question.add_choice('c2', False)

  question.add_choice('c3', False)

  question.add_choice('c4', False)

  question.add_choice('c5', False)

  id_true_2 = question.add_choice('c6', False).id
  swap_to_true.append(id_true_2)

  question.set_correct_choices(swap_to_true)

  for choice in question.choices:
    if choice.id == id_true_1 or choice.id == id_true_2:
      assert choice.is_correct
    else:
      assert not choice.is_correct

def test_set_correct_choice_invalid_id():
  question = Question('q1')

  question.add_choice('c1', False)
  question.add_choice('c2', False)
  question.add_choice('c3', False)

  with pytest.raises(Exception):
    question.set_correct_choices([-1, -2])
    question.set_correct_choices([ 4,  5])

def test_automatic_correction_of_correct_answer():
  question = Question('q1')

  question.add_choice('c1', False)
  question.add_choice('c2', False)
  question.add_choice('c3', False)
  question.add_choice('c4', True)

  results = question.correct_selected_choices([4])

  assert len(results) == 1
  assert results[0] == 4

def test_automatic_correction_of_wrong_answer():
  question = Question('q1')

  question.add_choice('c1', False)
  question.add_choice('c2', False)
  question.add_choice('c3', False)
  question.add_choice('c4', True)

  results = question.correct_selected_choices([1])

  assert len(results) == 0

def test_limit_of_selections():
  question1 = Question('q1', max_selections=2)

  question1.add_choice('c1', False)
  question1.add_choice('c2', False)
  question1.add_choice('c3', False)
  question1.add_choice('c4', True)
  question1.add_choice('c5', False)
  question1.add_choice('c6', False)
  question1.add_choice('c7', True)

  question2 = Question('q2', max_selections=4)
  
  question2.add_choice('c1', False)
  question2.add_choice('c2', False)
  question2.add_choice('c3', False)
  question2.add_choice('c4', True)
  question2.add_choice('c5', False)
  question2.add_choice('c6', False)
  question2.add_choice('c7', True)

  with pytest.raises(Exception):
    question1.correct_selected_choices([1,2,3])
    question2.correct_selected_choices([1,2,3,4,5])


  















