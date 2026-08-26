(module tests mzscheme
  
  (provide test-list)

  ;;;;;;;;;;;;;;;; tests ;;;;;;;;;;;;;;;;
  
  (define test-list
    '(
  
      ;; simple arithmetic
      (positive-const "11" 11)
      (negative-const "-33" -33)
      (simple-arith-1 "-(44,33)" 11)
  
      ;; nested arithmetic
      (nested-arith-left "-(-(44,33),22)" -11)
      (nested-arith-right "-(55, -(22,11))" 44)
  
      ;; simple variables
      (test-var-1 "x" 10)
      (test-var-2 "-(x,1)" 9)
      (test-var-3 "-(1,x)" -9)
      
      ;; simple unbound variables
      (test-unbound-var-1 "foo" error)
      (test-unbound-var-2 "-(x,foo)" error)
  
      ;; simple conditionals
      (if-true "if zero?(0) then 3 else 4" 3)
      (if-false "if zero?(1) then 3 else 4" 4)
      
      ;; test dynamic typechecking
      (no-bool-to-diff-1 "-(zero?(0),1)" error)
      (no-bool-to-diff-2 "-(1,zero?(0))" error)
      (no-int-to-if "if 1 then 2 else 3" error)

      ;; make sure that the test and both arms get evaluated
      ;; properly. 
      (if-eval-test-true "if zero?(-(11,11)) then 3 else 4" 3)
      (if-eval-test-false "if zero?(-(11, 12)) then 3 else 4" 4)
      
      ;; and make sure the other arm doesn't get evaluated.
      (if-eval-test-true-2 "if zero?(-(11, 11)) then 3 else foo" 3)
      (if-eval-test-false-2 "if zero?(-(11,12)) then foo else 4" 4)

      ;; simple let
      (simple-let-1 "let x = 3 in x" 3)

      ;; make sure the body and rhs get evaluated
      (eval-let-body "let x = 3 in -(x,1)" 2)
      (eval-let-rhs "let x = -(4,1) in -(x,1)" 2)

      ;; check nested let and shadowing
      (simple-nested-let "let x = 3 in let y = 4 in -(x,y)" -1)
      (check-shadowing-in-body "let x = 3 in let x = 4 in x" 4)
      (check-shadowing-in-rhs "let x = 3 in let x = -(x,1) in x" 2)

      ;; test plus-exp
      (simple-plus-exp-test "+(5, -(10,3))" 12)

      ;; test dot-exp
      (simple-dot-exp-test "*(5, -(10,3))" 35)

      ;; tests for greater-exp
      (simple-greater-exp-test1 "greater?(1,2)" #f)
      (simple-greater-exp-test2 "greater?(2,2)" #f)
      (simple-greater-exp-test3 "greater?(5,2)" #t)
      (complex-greater-exp-test "greater?(*(5, -(10,3)),2)" #t)

      ;; tests for arrow-exp - DELETED
      ;;(simple-arrow-exp-test1 "< greater?(5,2) ==> 3 >" 3)
      ;;(simple-arrow-exp-test2 "< greater?(1,2) ==> 5 >" #f)
      ;;(complex-arrow-exp-test1 "let x = 10 in < greater?(x,5) ==> 8 >" 8)

      ;; test cond-exp
      (simple-cond-exp-test "cond
< zero?(1) ==> 10 >
< greater?(5,3) ==> 20 >
else 30" 20)
      
      ))
  )