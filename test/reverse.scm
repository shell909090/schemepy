(define (reverse l)
  (define (rev l t)
    (if (null? l)
	t
	(rev (cdr l) (cons (car l) t))
	))
  (rev l '()))
(reverse '(1 2 3 4 5 6 7 8 9 10))
