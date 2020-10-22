
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'FALSE LPAREN NOT OPERATOR PROPOSITIONAL_VAR RPAREN TRUE\n        calc : expression\n        | empty\n    \n    empty :\n    \n    expression : expression OPERATOR expression\n    | expression OPERATOR PROPOSITIONAL_VAR\n    | expression OPERATOR TRUE\n    | expression OPERATOR FALSE\n    \n    expression_negated : NOT expression\n    | NOT expression_negated\n    | NOT TRUE\n    | NOT FALSE\n    | NOT PROPOSITIONAL_VAR\n    \n    expression : PROPOSITIONAL_VAR\n    | TRUE\n    | FALSE\n    | expression\n    | expression_negated\n    \n    expression : LPAREN expression RPAREN\n    '
    
_lr_action_items = {'PROPOSITIONAL_VAR':([0,8,9,10,],[4,4,16,18,]),'TRUE':([0,8,9,10,],[5,5,14,19,]),'FALSE':([0,8,9,10,],[6,6,15,20,]),'LPAREN':([0,8,9,10,],[8,8,8,8,]),'$end':([0,1,2,3,4,5,6,7,12,13,14,15,16,17,18,19,20,21,],[-3,0,-1,-2,-13,-14,-15,-17,-8,-9,-10,-11,-12,-4,-5,-6,-7,-18,]),'NOT':([0,8,9,10,],[9,9,9,9,]),'OPERATOR':([2,4,5,6,7,11,12,13,14,15,16,17,18,19,20,21,],[10,-13,-14,-15,-17,10,10,-9,-10,-11,-12,10,-5,-6,-7,-18,]),'RPAREN':([4,5,6,7,11,12,13,14,15,16,17,18,19,20,21,],[-13,-14,-15,-17,21,-8,-9,-10,-11,-12,-4,-5,-6,-7,-18,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'calc':([0,],[1,]),'expression':([0,8,9,10,],[2,11,12,17,]),'empty':([0,],[3,]),'expression_negated':([0,8,9,10,],[7,7,13,7,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> calc","S'",1,None,None,None),
  ('calc -> expression','calc',1,'p_calc','parser.py',104),
  ('calc -> empty','calc',1,'p_calc','parser.py',105),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',112),
  ('expression -> expression OPERATOR expression','expression',3,'p_expression','parser.py',117),
  ('expression -> expression OPERATOR PROPOSITIONAL_VAR','expression',3,'p_expression','parser.py',118),
  ('expression -> expression OPERATOR TRUE','expression',3,'p_expression','parser.py',119),
  ('expression -> expression OPERATOR FALSE','expression',3,'p_expression','parser.py',120),
  ('expression_negated -> NOT expression','expression_negated',2,'p_expression_negated','parser.py',126),
  ('expression_negated -> NOT expression_negated','expression_negated',2,'p_expression_negated','parser.py',127),
  ('expression_negated -> NOT TRUE','expression_negated',2,'p_expression_negated','parser.py',128),
  ('expression_negated -> NOT FALSE','expression_negated',2,'p_expression_negated','parser.py',129),
  ('expression_negated -> NOT PROPOSITIONAL_VAR','expression_negated',2,'p_expression_negated','parser.py',130),
  ('expression -> PROPOSITIONAL_VAR','expression',1,'p_expression_simple','parser.py',136),
  ('expression -> TRUE','expression',1,'p_expression_simple','parser.py',137),
  ('expression -> FALSE','expression',1,'p_expression_simple','parser.py',138),
  ('expression -> expression','expression',1,'p_expression_simple','parser.py',139),
  ('expression -> expression_negated','expression',1,'p_expression_simple','parser.py',140),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_parentesis','parser.py',146),
]
