(define (same-partiy a . l)
  (define (same-even a l)
    (cond ((null? l) '())
	  ((= a (remainder (car l) 2))
	   (cons (car l) (same-even a (cdr l))))
	  (else (same-even a (cdr l)))))
  (same-even (remainder a 2) l))
(same-partiy 1 3 4 5 6 7)
