(module data-structures (lib "eopl.ss" "eopl")

  (require "lang.scm")                  ; for expression?
  (require "store.scm")                 ; for reference?

  ;;(provide (all-defined))               ; too many things to list
  (provide (all-defined-out))
  
;;;;;;;;;;;;;;;; expressed values ;;;;;;;;;;;;;;;;

;;; an expressed value is either a number, a boolean, a procval, or a
;;; reference. 

  (define-datatype expval expval?
    (num-val
      (value number?))
    (bool-val
      (boolean boolean?))
    (proc-val 
      (proc proc?))
    (ref-val
      (ref reference?))
    )

  (define compare-types
    (lambda (typ1 typ2)
      (if (eqv? (type->symbol typ1) (type->symbol typ2))
          (bool-val #t) (bool-val #f)
        )
      ))

;;; extractors:
  (define type->symbol
    (lambda (v)
            (cases type v
              (int-type () 'int)
              (bool-type () 'bool)
              (func-type () 'func)
              (else (eopl:error 'type->symbol "unknown type ~s" v))
              )

            ))

   ;; overload value expression to type extractor
  (define expval->type
    (lambda (v)
      (cases expval v
        (num-val (num) (int-type))
        (bool-val (bool) (bool-type))
        (proc-val (proc) (func-type))
        (else
          (eopl:error 'expval->type "No overload type for value ~s" v)))))

  (define proc-param-type
    (lambda (p)
      (cases proc p
        (procedure (param-type bvar body env) param-type)
        (else
          (eopl:error 'proc-param-type "Expected a single procedure, got ~s" p)))))
  
  (define proc->list
    (lambda (p)
      (cases proc p
        (procedure (param-type bvar body env) (list p))
        (overloaded-procedure (procedures) procedures))))

  (define remove-procs-with-param-type
    (lambda (procedures target-type)
      (cond
        ((null? procedures) '())
        ((compare-types (proc-param-type (car procedures)) target-type)
         (remove-procs-with-param-type (cdr procedures) target-type))
        (else
         (cons (car procedures)
               (remove-procs-with-param-type (cdr procedures) target-type))))))

  ;; add new overload to proc (add to procedure overload list or override an existed one if its have the same signature)
  (define add-overload-to-proc
    (lambda (old-proc new-proc)
      (let ((new-type (proc-param-type new-proc)))
        (overloaded-procedure
          (cons new-proc
                (remove-procs-with-param-type
                  (proc->list old-proc)
                  new-type))))))

  (define expval->num
    (lambda (v)
      (cases expval v
	(num-val (num) num)
	(else (expval-extractor-error 'num v)))))

  (define expval->bool
    (lambda (v)
      (cases expval v
	(bool-val (bool) bool)
	(else (expval-extractor-error 'bool v)))))

  (define expval->proc
    (lambda (v)
      (cases expval v
	(proc-val (proc) proc)
	(else (expval-extractor-error 'proc v)))))

(define expval->ref
    (lambda (v)
      (cases expval v
	(ref-val (ref) ref)
	(else (expval-extractor-error 'reference v)))))

  (define expval-extractor-error
    (lambda (variant value)
      (eopl:error 'expval-extractors "Looking for a ~s, found ~s"
	variant value)))

;;;;;;;;;;;;;;;; procedures ;;;;;;;;;;;;;;;;

  (define-datatype proc proc?
    (procedure
     (type type?)
      (bvar symbol?)
      (body expression?)
      (env environment?))
    (overloaded-procedure
     (procedure (list-of proc?))
     )
    )

  (define-datatype environment environment?
    (empty-env)
    (extend-env 
      (bvar symbol?)
      (bval reference?)                 ; new for implicit-refs
      (saved-env environment?))
    (extend-env-rec*
      (proc-names (list-of symbol?))
      (param-types (list-of type?))
      (b-vars (list-of symbol?))
      (proc-bodies (list-of expression?))
      (saved-env environment?)))

  ;; env->list : Env -> List
  ;; used for pretty-printing and debugging
  (define env->list
    (lambda (env)
      (cases environment env
	(empty-env () '())
	(extend-env (sym val saved-env)
	  (cons
	    (list sym val)              ; val is a denoted value-- a
                                        ; reference. 
	    (env->list saved-env)))
	(extend-env-rec* (p-names param-types b-vars p-bodies saved-env)
	  (cons
	    (list 'letrec p-names '...)
	    (env->list saved-env))))))

  ;; expval->printable : ExpVal -> List
  ;; returns a value like its argument, except procedures get cleaned
  ;; up with env->list 
  (define expval->printable
    (lambda (val)
      (cases expval val
        (proc-val (p)
          (cases proc p
            (procedure (param-type var body saved-env)
              (list 'procedure (type->symbol param-type) var '... (env->list saved-env)))
            (overloaded-procedure (procedures)
              (cons 'overloaded-procedure
                (map
                  (lambda (proc1)
                    (cases proc proc1
                      (procedure (param-type var body saved-env)
                        (list (type->symbol param-type) var '...))
                      (else proc1)))
                  procedures)))))
        (else val))))

)