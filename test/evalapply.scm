(display (eval '(+ 1 1)))
(define (test-eval n)
  (eval '(+ n n) (current-environment)))
(display (test-eval 10))
