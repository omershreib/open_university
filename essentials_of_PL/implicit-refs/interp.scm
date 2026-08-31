(module interp (lib "eopl.ss" "eopl")
  
  ;; interpreter for the IMPLICIT-REFS language

  (require "drscheme-init.scm")

  (require "lang.scm")
  (require "data-structures.scm")
  (require "environments.scm")
  (require "store.scm")
  
  (provide value-of-program value-of instrument-let instrument-newref)

;;;;;;;;;;;;;;;; switches for instrument-let ;;;;;;;;;;;;;;;;

  (define instrument-let (make-parameter #f))

  ;; say (instrument-let #t) to turn instrumentation on.
  ;;     (instrument-let #f) to turn it off again.

;;;;;;;;;;;;;;;; the interpreter ;;;;;;;;;;;;;;;;

  ;; value-of-program : Program -> ExpVal
  (define value-of-program 
    (lambda (pgm)
      (initialize-store!)
      (cases program pgm
        (a-program (exp1)
          (value-of exp1 (init-env))))))

  ;; value-of : Exp * Env -> ExpVal
  ;; Page: 118, 119
  (define value-of
    (lambda (exp env)
      (cases expression exp

        ;\commentbox{ (value-of (const-exp \n{}) \r) = \n{}}
        (const-exp (num) (num-val num))

        ;\commentbox{ (value-of (var-exp \x{}) \r) 
        ;              = (deref (apply-env \r \x{}))}
        (var-exp (var) (deref (apply-env env var)))

        ;\commentbox{\diffspec}
        (diff-exp (exp1 exp2)
          (let ((val1 (value-of exp1 env))
                (val2 (value-of exp2 env)))
            (let ((num1 (expval->num val1))
                  (num2 (expval->num val2)))
              (num-val
                (- num1 num2)))))

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

        ;\commentbox{\ma{\theletspecsplit}}
        (let-exp (var exp1 body)       
          (let ((v1 (value-of exp1 env)))
            (value-of body
              (extend-env var (newref v1) env))))
        
        (proc-exp (typ var body)
                       (proc-val (procedure typ var body env)))
                      
                      
         

        (call-exp (rator rand)
          (let ((proc (expval->proc (value-of rator env)))
                (arg (value-of rand env)))
            (apply-procedure proc arg)))

        (letrec-exp (p-names b-vars p-bodies letrec-body)
          (value-of letrec-body
            (extend-env-rec* p-names b-vars p-bodies env)))

        (begin-exp (exp1 exps)
          (letrec 
            ((value-of-begins
               (lambda (e1 es)
                 (let ((v1 (value-of e1 env)))
                   (if (null? es)
                     v1
                     (value-of-begins (car es) (cdr es)))))))
            (value-of-begins exp1 exps)))

        (assign-exp (var exp1)
          (begin
            (setref!
              (apply-env env var)
              (value-of exp1 env))
            (num-val 27)))

        (swap-exp (var1 var2)
                  (let ((ref1 (apply-env env var1))
                        (ref2 (apply-env env var2)))

                    (let ((val1 (deref ref1))
                          (val2 (deref ref2)))

                    (setref! ref2 val1)
                    (setref! ref1 val2))))

        (inc-exp (var1)
                 (let ((ref1 (apply-env env var1)))
                   (let ((val1 (deref ref1)))
                     (let ((num1 (expval->num val1)))
                       (setref! ref1 (num-val (+ num1 1)))
                 ))))

        (exchange-if-exp (cond-exp var1 var2)
                         (let ((cond
                                 (expval->bool
                                  (value-of cond-exp env))))

                           (if cond
                               (begin
                                 (value-of (swap-exp var1 var2) env)
                                 (bool-val #t))
                               (bool-val #f))))


        (overload-exp (pname-var typ var body)
                   (let ((pname-ref (apply-env env pname-var)))
                     (let ((pname-val (deref pname-ref)))
                       (cases expval pname-val
                         (proc-val (p)
                                   (extend-env
                                    ((proc-val
                                      (procedure typ var body env))
                                                      env))
                                   )
                         (num-val (n)
                                  (eopl:error 'overload-exp "cannot overload non procedure ~s"
                                               pname-val)
                                  )
                         (ref-val (r)
                                  (eopl:error 'overload-exp "cannot overload non procedure ~s"
                                               pname-val)
                                  )
                         (bool-val (b)
                                  (eopl:error 'overload-exp "cannot overload non procedure ~s"
                                               pname-val)
                                  )
                         )
                       
                       )))

        )))


  ;; apply-procedure : Proc * ExpVal -> ExpVal
  ;; Page: 119

  ;; uninstrumented version
  ;;  (define apply-procedure
  ;;    (lambda (proc1 val)
  ;;      (cases proc proc1
  ;;        (procedure (var body saved-env)
  ;;          (value-of body
  ;;            (extend-env var (newref val) saved-env))))))
  
  ;; instrumented version
  (define apply-procedure
    (lambda (proc1 arg)
      (cases proc proc1
        (procedure (param-type var body saved-env)
          (if (compare-types param-type (expval->type arg))
            (let ((r (newref arg)))
              (let ((new-env (extend-env var r saved-env)))
                (when (instrument-let)
                  (begin
                    (eopl:printf
                      "entering body of proc ~s with env =~%"
                      var)
                    (pretty-print (env->list new-env)) 
                    (eopl:printf "store =~%")
                    (pretty-print (store->readable (get-store-as-list)))
                    (eopl:printf "~%")))
                (value-of body new-env)))
            (eopl:error 'apply-procedure
              "Procedure expected argument of type ~s, but got ~s"
              (type->symbol param-type)
              (type->symbol (expval->type arg)))))
        (overloaded-procedure (procedures)
          (let ((arg-type (expval->type arg)))
            (letrec
              ((find-matching-proc
                 (lambda (procs)
                   (cond
                     ((null? procs) #f)
                     ((compare-types (proc-param-type (car procs)) arg-type) (car procs))
                     (else (find-matching-proc (cdr procs)))))))
              (let ((matching-proc (find-matching-proc procedures)))
                (if matching-proc
                  (apply-procedure matching-proc arg)
                  (eopl:error 'apply-procedure
                    "No overloaded version for argument type ~s"
                    (type->symbol arg-type))))))))))  

  ;; store->readable : Listof(List(Ref,Expval)) 
  ;;                    -> Listof(List(Ref,Something-Readable))
  (define store->readable
    (lambda (l)
      (map
        (lambda (p)
          (list
            (car p)
            (expval->printable (cadr p))))
        l)))

  

  )
  


  
