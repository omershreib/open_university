(module interp (lib "eopl.ss" "eopl")
  
  ;; interpreter for the LET language.  The \commentboxes are the
  ;; latex code for inserting the rules into the code in the book.
  ;; These are too complicated to put here, see the text, sorry.

  ;;; Remember: interp.scm define how commands are implemented
  ;;;           according to lambda-expression rules

  (require "drscheme-init.scm")

  (require "lang.scm")
  (require "data-structures.scm")
  (require "environments.scm")

  (provide value-of-program value-of)



;;;;;;;;;;;;;;;; my implementations ;;;;;;;;;;;;;;;;

  ;; not used. just check I know how to implement
  ;; addition from a language with only diff (-) supports
  ;; this becuase this course is for masochists 
  (define apply-plus
    (lambda (num1 num2)
      (- num1 (- 0 num2))
      ))
  
  (define apply-dot
    (lambda (num1 num2)
      (define apply-dot-rec
        (lambda (n remain)
          (if (zero? remain) 0
              (+ n
                 (apply-dot-rec n (- remain 1)))
              )
          ))
      (apply-dot-rec num1 num2)
      ))


;;; helper(s) for cond-exp
  (define value-of-cond
    (lambda (conditions results else-exp env)
      (if (null? conditions)

          ;; no condition was true
          (value-of else-exp env)

          ;; if conditions is not-empty, check if the first-left
          ;; condition is true
          (let ((cond-val (value-of (car conditions) env)))

            (if (expval->bool cond-val)

                ;; this condition is true ==> return its result
                (value-of (car results) env)

                ;; condition is false
                ;; then check the next condition if avaliable
                (value-of-cond (cdr conditions) (cdr results) else-exp env)
                )
            )
          
          )
      ))

;;; helper(s) for multi-let-exp

  (define initialize-let-env
    (lambda (vars exps env)
      (if (null? vars) env
          (let ((val (value-of (car exps) env)))
            (initialize-let-env
             (cdr vars)
             (cdr exps)
             (extend-env (car vars) val env))
            ))
          ))


  (define run-let-body
    (lambda (vars exps body let-env)

      ;;???
      ))
      

;;;;;;;;;;;;;;;; the interpreter ;;;;;;;;;;;;;;;;

  ;; value-of-program : Program -> ExpVal
  ;; Page: 71
  (define value-of-program 
    (lambda (pgm)
      (cases program pgm
        (a-program (exp1)
          (value-of exp1 (init-env))))))

  ;; value-of : Exp * Env -> ExpVal
  ;; Page: 71
  (define value-of
    (lambda (exp env)
      (cases expression exp

        ;\commentbox{ (value-of (const-exp \n{}) \r) = \n{}}
        (const-exp (num) (num-val num))

        ;\commentbox{ (value-of (var-exp \x{}) \r) = (apply-env \r \x{})}
        (var-exp (var) (apply-env env var))

        ;\commentbox{\diffspec}
        (diff-exp (exp1 exp2)
          (let ((val1 (value-of exp1 env))
                (val2 (value-of exp2 env)))
            (let ((num1 (expval->num val1))
                  (num2 (expval->num val2)))
              (num-val
                (- num1 num2)))))

        ;\commentbox{\plusspec}
        (plus-exp (exp1 exp2)
          (let ((val1 (value-of exp1 env))
                (val2 (value-of exp2 env)))
            (let ((num1 (expval->num val1))
                  (num2 (expval->num val2)))
              (num-val
                (+ num1 num2)))))

        ;\commentbox{\dotspec}
        (dot-exp (exp1 exp2)
          (let ((val1 (value-of exp1 env))
                (val2 (value-of exp2 env)))
            (let ((num1 (expval->num val1))
                  (num2 (expval->num val2)))
              (num-val
                (apply-dot num1 num2)))))

        ;\commentbox{\zerotestspec}
        (zero?-exp (exp1)
          (let ((val1 (value-of exp1 env)))
            (let ((num1 (expval->num val1)))
              (if (zero? num1)
                (bool-val #t)
                (bool-val #f)))))
              
        ;\commentbox{\ma{\theifspec}}
        (if-exp (exp1 exp2 exp3)
          (let ((val1 (value-of exp1 env)))
            (if (expval->bool val1)
              (value-of exp2 env)
              (value-of exp3 env))))

        ;; old let-exp
        ;\commentbox{\ma{\theletspecsplit}}
        #|
        (let-exp (var exp1 body)       
          (let ((val1 (value-of exp1 env)))
            (value-of body
              (extend-env var val1 env))))
        |#

        ;\commentbox{\ma{\multiletspecsplit}}
        (let-exp (vars exps body)
                 (let ((let-env
                        (initialize-let-env vars exps env)))
                   (run-let-body vars exps body let-env)
                   ))
                 
                 

        ;\commentbox{\greaterspec}
        (greater-exp (exp1 exp2)
          (let ((val1 (value-of exp1 env))
                (val2 (value-of exp2 env)))
            (let ((num1 (expval->num val1))
                  (num2 (expval->num val2)))
              (bool-val
                (positive? (- num1 num2))))))

        ;\commentbox{\arrowspec}
        #|(arrow-exp (exp1 exp2)
          (let ((val1 (value-of exp1 env))
                (val2 (value-of exp2 env)))
            (let ((bool1 (expval->bool val1))
                  (num2 (expval->num val2)))
              (if (eqv? bool1 #t) val2 (bool-val #f))
              )))
        |#
                   
                   

        ;\commentbox{\condspec}
        ;; in modus-ponens (if->then) the "if" is the prefix and the "then" is the suffix
        ;; call the first case line that their suffix is positive
        (cond-exp (conditions results else-exp)

                  (value-of-cond conditions results else-exp env)
                  )
        
        )))


  )

