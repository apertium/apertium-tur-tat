#lang racket

; Racket interface for apertium-tur-tat
;
; REQUIRES: apertiumpp package.
; https://taruen.github.io/apertiumpp/apertiumpp/ gives info on how to install
; it.

(provide tat-tur
         tat-tur-from-pretransfer-to-biltrans
         tat-tur-from-t1x-to-postgen)

(require pkg/lib
         rackunit
         rash
         apertiumpp/streamparser)

(define (symbol-append s1 s2)
  (string->symbol (string-append (symbol->string s1) (symbol->string s2))))

(define A-TUR-TAT './)
(define A-TAT-TUR-BIL (symbol-append A-TUR-TAT 'tat-tur.autobil.bin))
(define A-TAT-TUR-T1X (symbol-append A-TUR-TAT 'apertium-tur-tat.tat-tur.t1x))
(define A-TAT-TUR-T1X-BIN (symbol-append A-TUR-TAT 'tat-tur.t1x.bin))
(define A-TAT-TUR-T2X (symbol-append A-TUR-TAT 'apertium-tur-tat.tat-tur.t2x))
(define A-TAT-TUR-T2X-BIN (symbol-append A-TUR-TAT 'tat-tur.t2x.bin))
(define A-TAT-TUR-T3X (symbol-append A-TUR-TAT 'apertium-tur-tat.tat-tur.t3x))
(define A-TAT-TUR-T3X-BIN (symbol-append A-TUR-TAT 'tat-tur.t3x.bin))
(define A-TAT-TUR-T4X (symbol-append A-TUR-TAT 'apertium-tur-tat.tat-tur.t4x))
(define A-TAT-TUR-T4X-BIN (symbol-append A-TUR-TAT 'tat-tur.t4x.bin))
(define A-TAT-TUR-GEN (symbol-append A-TUR-TAT 'tat-tur.autogen.bin))
(define A-TAT-TUR-PGEN (symbol-append A-TUR-TAT 'tat-tur.autopgen.bin))

(define (tat-tur s)
  (parameterize ([current-directory (pkg-directory "apertium-tur-tat")])
    (rash
     "echo (values s) | apertium -d . tat-tur")))

(define (tat-tur-from-pretransfer-to-biltrans s)
  (parameterize ([current-directory (pkg-directory "apertium-tur-tat")])
    (rash
     "echo (values s) | apertium-pretransfer | "
     "lt-proc -b (values A-TAT-TUR-BIL)")))

(define (tat-tur-from-t1x-to-postgen s)
  (parameterize ([current-directory (pkg-directory "apertium-tur-tat")])
    (rash
     "echo (values s) | "
     "apertium-transfer -b (values A-TAT-TUR-T1X) (values A-TAT-TUR-T1X-BIN) | "
     "apertium-interchunk (values A-TAT-TUR-T2X) (values A-TAT-TUR-T2X-BIN) | "
     "apertium-postchunk (values A-TAT-TUR-T3X) (values A-TAT-TUR-T3X-BIN) | "
     "apertium-transfer -n (values A-TAT-TUR-T4X) (values A-TAT-TUR-T4X-BIN) | "      
     "lt-proc -g (values A-TAT-TUR-GEN) | "
     "lt-proc -p (values A-TAT-TUR-PGEN)"))) 
