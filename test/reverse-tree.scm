(define (list-reverse l)
  (define (inner l t)
    (if (null? l)
	t
	(inner (cdr l) (cons (car l) t))))
  (inner l '()))
(define (reverse t)
  (list-reverse (map list-reverse t)))
(reverse '((1 2) (3 4)))
