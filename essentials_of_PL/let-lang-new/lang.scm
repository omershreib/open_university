(module lang

  ;; grammar for the LET language

  ;; Remember: lang.scm defines the grammer of language
  ;;           (how commands are being written)

  (lib "eopl.ss" "eopl")                
  
  (require "drscheme-init.scm")
  
  (provide (all-defined-out))

  ;;;;;;;;;;;;;;;; grammatical specification ;;;;;;;;;;;;;;;;
  
  (define the-lexical-spec
    '((whitespace (whitespace) skip)
      (comment ("%" (arbno (not #\newline))) skip)
      (identifier
       (letter (arbno (or letter digit "_" "-" "?")))
       symbol)
      (number (digit (arbno digit)) number)
      (number ("-" digit (arbno digit)) number)
      ))
  
  (define the-grammar
    '((program (expression) a-program)

      (expression (number) const-exp)
      (expression
        ("-" "(" expression "," expression ")")
        diff-exp)


      ;; exercises 1.1: plus-exp
      (expression
       ("+" "(" expression "," expression ")")
       plus-exp
       )

      ;; exercises 1.2: dot-exp
      (expression
       ("*" "(" expression "," expression ")")
       dot-exp)


      ;; exercises 1.3: greater-exp
      (expression
       ("greater?" "(" expression "," expression ")")
       greater-exp)


      ;; needed (I think) to implement cond-exp
      ;; arrow-exp - DELETED
      ;;(expression
      ;; ("<" expression "==>" expression ">")
      ;; arrow-exp)

      ;; exercises 1.4: cond-exp
      (expression
       ("cond"
        (arbno "<" expression "==>" expression ">")
        "else" expression)
       cond-exp)
      
      
      
      (expression
       ("zero?" "(" expression ")")
       zero?-exp)

      (expression
       ("if" expression "then" expression "else" expression)
       if-exp)

      (expression (identifier) var-exp)

      ;; old-let
      #|
      (expression
       ("let" identifier "=" expression "in" expression)
       let-exp)
      |#

      ;; exercise 5: edit let-exp to support multi-let
      (expression
       ("let"
        (arbno identifier "=" expression)
        "in" expression)
       let-exp)

      ;; exercise 6: implements sequential let* 
      (expression
       ("let*"
        (arbno identifier "=" expression)
        "in" expression)
       letstar-exp)


      ;; exercise 7: for-exp (spiced with steps)
      (expression
       ("for" identifier "=" expression
              "to" expression
              "step" expression
              "do" expression)
       for-exp)
      
      ))

     
  
  ;;;;;;;;;;;;;;;; sllgen boilerplate ;;;;;;;;;;;;;;;;
  
  (sllgen:make-define-datatypes the-lexical-spec the-grammar)
  
  (define show-the-datatypes
    (lambda () (sllgen:list-define-datatypes the-lexical-spec the-grammar)))
  
  (define scan&parse
    (sllgen:make-string-parser the-lexical-spec the-grammar))
  
  (define just-scan
    (sllgen:make-string-scanner the-lexical-spec the-grammar))
  
  )
