;; 八皇后问题
;; 传说中的reduce
(define (accumulate op initial sequence)
  (if (null? sequence) initial
      (op (car sequence)
	  (accumulate op initial (cdr sequence)))))
;; 平行映射，对seq中的每个元素x，取(proc x)为一个列表。(flatmap proc seq)为所有列表的总和。
(define (flatmap proc seq)
  (accumulate append '() (map proc seq)))
;; 生成[a, b]的区间序列
(define (enumerate-interval a b)
  (if (>= a b)
      (list b)
      (cons a (enumerate-interval (+ a 1) b))))
(define (queens board-size)
  (define (queen-cols i)
    (if (= i 0)
	(list (empty-board))
	(filter
	 (lambda (positions) (safe? positions))
	 (flatmap
	  (lambda (rest-of-queens)
	    (map (lambda (j)
		   (adjoin-position i j rest-of-queens))
		 (enumerate-interval 1 board-size)))
	  (queen-cols (- i 1))))
	))
  (queen-cols board-size)
  )
(define (empty-board) (list))
(define (adjoin-position i j rest-of-queens)
  (cons (cons i j) rest-of-queens))
(define (safe? positions)
  (define (safe-row? j positions)
    (eq? '()
	 (filter (lambda (y) (= y j))
		 (map (lambda (p) (cdr p)) (cdr positions))
		 )))
  (define (safe-add? s positions)
    (eq? '()
	 (filter (lambda (e) (= e s))
		 (map (lambda (p) (+ (car p) (cdr p))) (cdr positions))
		 )))
  (define (safe-dec? d positions)
    (eq? '()
	 (filter (lambda (e) (= e d))
		 (map (lambda (p) (- (car p) (cdr p))) (cdr positions))
		 )))
  (and (safe-row? (cdar positions) positions)
       (safe-add? (+ (caar positions) (cdar positions)) positions)
       (safe-dec? (- (caar positions) (cdar positions)) positions))
  )
(display (queens 8))
(newline)
;; X O O O O O O O
;; O O O O X O O O
;; O O O O O O O X
;; O O O O O X O O
;; O O X O O O O O
;; O O O O O O X O
;; O X O O O O O O
;; O O O X O O O O