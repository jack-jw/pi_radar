FasdUAS 1.101.10   ��   ��    k             l     ��  ��      Pi-radar Utility     � 	 	 "   P i - r a d a r   U t i l i t y   
  
 l     ��������  ��  ��        l     ��  ��     
 Main menu     �      M a i n   m e n u      l     ����  r         l     ����  n         1    ��
�� 
bhit  l     ����  I    ��  
�� .sysodisAaleR        TEXT  m        �     P i - r a d a r   U t i l i t y  ��  
�� 
btns  J          ! " ! m     # # � $ $  Q u i t "  % & % m     ' ' � ( (   M a n a g e   D a t a b a s e s &  )�� ) m     * * � + +   F l a s h   t o   S D   C a r d��    �� ,��
�� 
dflt , m    	���� ��  ��  ��  ��  ��    o      ����  0 mainmenureturn mainMenuReturn��  ��     -�� - l  � . / 0 . Z   � 1 2 3�� 1 =    4 5 4 o    ����  0 mainmenureturn mainMenuReturn 5 m     6 6 � 7 7   F l a s h   t o   S D   C a r d 2 k     8 8  9 : 9 I   �� ;��
�� .sysodisAaleR        TEXT ; m     < < � = =  N o t   i m p l e m e n t e d��   :  >�� > l   ��������  ��  ��  ��   3  ? @ ? =  " % A B A o   " #����  0 mainmenureturn mainMenuReturn B m   # $ C C � D D   M a n a g e   D a t a b a s e s @  E�� E k   (� F F  G H G r   ( : I J I l  ( 6 K���� K n   ( 6 L M L 1   4 6��
�� 
bhit M l  ( 4 N���� N I  ( 4�� O P
�� .sysodisAaleR        TEXT O m   ( ) Q Q � R R   M a n a g e   D a t a b a s e s P �� S T
�� 
btns S J   * . U U  V W V m   * + X X � Y Y $ L o a d   C u s t o m   R o u t e s W  Z�� Z m   + , [ [ � \ \   U p d a t e   D a t a b a s e s��   T �� ]��
�� 
dflt ] m   / 0���� ��  ��  ��  ��  ��   J o      ���� 0 dbmenureturn dbMenuReturn H  ^ _ ^ l  ; ;��������  ��  ��   _  ` a ` l  ;� b c d b Z   ;� e f g�� e =  ; B h i h o   ; >���� 0 dbmenureturn dbMenuReturn i m   > A j j � k k   U p d a t e   D a t a b a s e s f k   E� l l  m n m I  E V�� o p
�� .sysodisAaleR        TEXT o m   E H q q � r r   U p d a t e   D a t a b a s e s p �� s t
�� 
mesS s m   K N u u � v v � E n s u r e   y o u r   U S B   d i s k   i s   c o n n e c t e d   t o   t h i s   c o m p u t e r   a n d   i s   v i s i b l e   i n   F i n d e r ,   a n d   t h a t   y o u   a r e   c o n n e c t e d   t o   t h e   I n t e r n e t . t �� w��
�� 
btns w m   O R x x � y y  C o n t i n u e��   n  z { z l  W W��������  ��  ��   {  | } | l  W W�� ~ ��   ~  
 Get disks     � � �    G e t   d i s k s }  � � � r   W f � � � n   W b � � � 2  ^ b��
�� 
cpar � l  W ^ ����� � I  W ^�� ���
�� .sysoexecTEXT���     TEXT � m   W Z � � � � �  l s   / V o l u m e s /��  ��  ��   � o      ���� 0 disklist diskList �  � � � l  g g��������  ��  ��   �  � � � l  g g�� � ���   �    Remove Time Machine disks    � � � � 4   R e m o v e   T i m e   M a c h i n e   d i s k s �  � � � r   g m � � � J   g i����   � o      ���� 0 filtereddisks filteredDisks �  � � � X   n � ��� � � Z   � � � ����� � H   � � � � E   � � � � � o   � ����� 0 disk   � m   � � � � � � �  B a c k u p s   o f   � r   � � � � � o   � ����� 0 disk   � n       � � �  ;   � � � o   � ����� 0 filtereddisks filteredDisks��  ��  �� 0 disk   � o   q t���� 0 disklist diskList �  � � � l  � ���������  ��  ��   �  � � � l  � ��� � ���   � + % Prompt user to select their USB disk    � � � � J   P r o m p t   u s e r   t o   s e l e c t   t h e i r   U S B   d i s k �  � � � r   � � � � � I  � ��� � �
�� .gtqpchltns    @   @ ns   � o   � ����� 0 filtereddisks filteredDisks � �� � �
�� 
prmp � m   � � � � � � � ( S e l e c t   y o u r   U S B   d i s k � �� � �
�� 
inSL � J   � �����   � �� � �
�� 
mlsl � m   � ���
�� boovfals � �� ���
�� 
empL��   � o      ���� 0 
chosendisk 
chosenDisk �  � � � l  � ���������  ��  ��   �  � � � l  �� � � � � Z   �� � ����� � >  � � � � � o   � ����� 0 
chosendisk 
chosenDisk � m   � ���
�� boovfals � k   �� � �  � � � r   � � � � � n   � � � � � 4   � ��� �
�� 
cobj � m   � �����  � o   � ����� 0 
chosendisk 
chosenDisk � o      ���� 0 selecteddisk selectedDisk �  � � � l  � ���������  ��  ��   �  � � � r   � � � � � I  � ��� ���
�� .sysoexecTEXT���     TEXT � l  � � ����� � b   � � � � � b   � � � � � m   � � � � � � � . d i s k u t i l   i n f o   / V o l u m e s / � n   � � � � � 1   � ���
�� 
strq � o   � ����� 0 selecteddisk selectedDisk � m   � � � � � � � �   |   g r e p   ' F i l e   S y s t e m   P e r s o n a l i t y '   |   a w k   ' / F i l e   S y s t e m   P e r s o n a l i t y /   { p r i n t   $ 4 } '��  ��  ��   � o      ���� 0 diskfs diskFS �  � � � r   � � � � I  � ��� ���
�� .sysoexecTEXT���     TEXT � l  � � ����� � b   � � � � � b   � � � � � m   � � � � � � � . d i s k u t i l   i n f o   / V o l u m e s / � n   � � � � � 1   � ���
�� 
strq � o   � ����� 0 selecteddisk selectedDisk � m   � � � � � � � t   |   g r e p   ' P a r t   o f   W h o l e '   |   a w k   ' / P a r t   o f   W h o l e /   { p r i n t   $ 4 } '��  ��  ��   � o      ���� 0 
diskparent 
diskParent �  � � � l ��������  ��  ��   �  � � � l � � � � � Z  � � ��� � � = 
 � � � o  ���� 0 diskfs diskFS � m  	 � � � � �  M S - D O S � k  { � �  � � � I 3�� 
�� .sysodisAaleR        TEXT  l ���� m   � & E r a s e   &   F o r m a t   D i s k��  ��   ��
�� 
mesS l ���� b  	 b  

 m   � T h e   e n t i r e t y   o f   t h e   d i s k ,   i n c l u d i n g   a n y   o t h e r   p a r t i t i o n s   w i t h i n   i t ,   w i l l   b e   e r a s e d   a n d   f o r m a t t e d .   P l e a s e   r e m o v e   a n y   i m p o r t a n t   d a t a   f r o m   o  �� 0 selecteddisk selectedDisk	 m   �$   b e f o r e   p r o c e e d i n g .   T h i s   m a y   t a k e   a   w h i l e ,   d o   n o t   c l o s e   t h i s   a p p l i c a t i o n ,   r e m o v e   t h e   d i s k   o r   t u r n   o f f   y o u r   c o m p u t e r .   T h i s   a c t i o n   c a n n o t   b e   u n d o n e .��  ��   �~
�~ 
btns J  +  m  " �  C a n c e l �} l ")�|�{ b  ") m  "% �  E r a s e   &   F o r m a t   o  %(�z�z 0 selecteddisk selectedDisk�|  �{  �}   �y�x
�y 
dflt m  ,-�w�w �x   � �v Z  4{ �u�t > 4=!"! l 49#�s�r# n  49$%$ 1  79�q
�q 
bhit% l 47&�p�o& 1  47�n
�n 
rslt�p  �o  �s  �r  " m  9<'' �((  C a n c e l  k  @w)) *+* l @@�m�l�k�m  �l  �k  + ,-, r  @I./. m  @C�j�j / 1  CH�i
�i 
ppgt- 010 r  JS232 m  JM44 �55 < E r a s i n g   a n d   f o r m a t t i n g   d i s k . . .3 1  MR�h
�h 
ppgd1 676 l TT�g�f�e�g  �f  �e  7 898 r  T[:;: m  TU�d�d  ; 1  UZ�c
�c 
ppgc9 <=< l \\�b�a�`�b  �a  �`  = >?> r  \e@A@ m  \_BB �CC B D o w n l o a d i n g   c a l l s i g n s   d a t a b a s e . . .A 1  _d�_
�_ 
ppga? DED r  f�FGF c  fHIH n  f{JKJ 1  w{�^
�^ 
psxpK l fwL�]�\L I fw�[MN
�[ .sysorpthalis        TEXTM m  fiOO �PP  c a l l s i g n s . p yN �ZQ�Y
�Z 
in BQ l lsR�X�WR I ls�VS�U
�V .earsffdralis        afdrS m  loTT�                                                                                      @ alis    �  Macintosh HD               ��BD ����Pi-radar Utility.app                                           ������        ����  
 cu             utility   K/:Users:jackwoodward:Documents:ADS-B receiver:utility:Pi-radar Utility.app/   *  P i - r a d a r   U t i l i t y . a p p    M a c i n t o s h   H D  HUsers/jackwoodward/Documents/ADS-B receiver/utility/Pi-radar Utility.app  /    ��  �U  �X  �W  �Y  �]  �\  I m  {~�T
�T 
TEXTG o      �S�S *0 callsignfetcherpath callsignFetcherPathE UVU I ���RW�Q
�R .sysoexecTEXT���     TEXTW b  ��XYX b  ��Z[Z m  ��\\ �]]  p y t h o n 3   '[ o  ���P�P *0 callsignfetcherpath callsignFetcherPathY m  ��^^ �__  '�Q  V `a` r  ��bcb m  ���O�O c 1  ���N
�N 
ppgca ded l ���M�L�K�M  �L  �K  e fgf r  ��hih m  ��jj �kk Z D o w n l o a d i n g   B r i t i s h   A i r w a y s   r o u t e   d a t a b a s e . . .i 1  ���J
�J 
ppgag lml r  ��non c  ��pqp n  ��rsr 1  ���I
�I 
psxps l ��t�H�Gt I ���Fuv
�F .sysorpthalis        TEXTu m  ��ww �xx  r o u t e s B A W . p yv �Ey�D
�E 
in By l ��z�C�Bz I ���A{�@
�A .earsffdralis        afdr{ m  ��||�                                                                                      @ alis    �  Macintosh HD               ��BD ����Pi-radar Utility.app                                           ������        ����  
 cu             utility   K/:Users:jackwoodward:Documents:ADS-B receiver:utility:Pi-radar Utility.app/   *  P i - r a d a r   U t i l i t y . a p p    M a c i n t o s h   H D  HUsers/jackwoodward/Documents/ADS-B receiver/utility/Pi-radar Utility.app  /    ��  �@  �C  �B  �D  �H  �G  q m  ���?
�? 
TEXTo o      �>�> 0 routesbawpath routesBAWPathm }~} I ���=�<
�= .sysoexecTEXT���     TEXT b  ����� b  ����� m  ���� ���  p y t h o n 3   '� o  ���;�; 0 routesbawpath routesBAWPath� m  ���� ���  '�<  ~ ��� r  ����� m  ���:�: � 1  ���9
�9 
ppgc� ��� l ���8�7�6�8  �7  �6  � ��� r  ����� m  ���� ��� B D o w n l o a d i n g   a i r f r a m e s   d a t a b a s e . . .� 1  ���5
�5 
ppga� ��� I ���4��3
�4 .sysoexecTEXT���     TEXT� m  ���� ��� � c d   ~ / D o w n l o a d s ;   c u r l   - o   / t m p / a i r f r a m e s . c s v   h t t p s : / / o p e n s k y - n e t w o r k . o r g / d a t a s e t s / m e t a d a t a / a i r c r a f t D a t a b a s e . c s v�3  � ��� r  ����� m  ���2�2 � 1  ���1
�1 
ppgc� ��� l ���0�/�.�0  �/  �.  � ��� r  ����� m  ���� ��� , F o r m a t t i n g   U S B   d i s k . . .� 1  ���-
�- 
ppga� ��� I  �,��+
�, .sysoexecTEXT���     TEXT� b   ��� m   �� ��� ` d i s k u t i l   e r a s e D i s k   F A T 3 2   P I R A D A R   M B R F o r m a t   / d e v /� o  �*�* 0 
diskparent 
diskParent�+  � ��� r  ��� m  �)�) � 1  �(
�( 
ppgc� ��� l �'�&�%�'  �&  �%  � ��� r  ��� m  �� ��� * T r a n s f e r r i n g   f i l e s . . .� 1  �$
�$ 
ppga� ��� I %�#��"
�# .sysoexecTEXT���     TEXT� m  !�� ���� m k d i r   / V o l u m e s / P I R A D A R / . p i - r a d a r ;   m v   / t m p / c a l l s i g n s . c s v   / V o l u m e s / P I R A D A R / . p i - r a d a r / c a l l s i g n s . c s v ;   m v   / t m p / r o u t e s B A W . c s v   / V o l u m e s / P I R A D A R / . p i - r a d a r / r o u t e s B A W . c s v ;   m v   / t m p / a i r f r a m e s . c s v   / V o l u m e s / P I R A D A R / . p i - r a d a r / a i r f r a m e s . c s v ;�"  � ��� l &&�!� ��!  �   �  � ��� I &-���
� .sysoexecTEXT���     TEXT� m  &)�� ���j e c h o   ' P l e a s e   i n s e r t   t h i s   U S B   i n   t o   t h e   R a s p b e r r y   P i   r u n n i n g   P i - r a d a r .   T h i s   f i l e   w i l l   b e   d e l e t e d   o n c e   t h e   d a t a b a s e s   h a v e   b e e n   s u c c e s s f u l l y   t r a n s f e r r e d . '   >   / V o l u m e s / P I R A D A R / R E A D M E . t x t�  � ��� r  .7��� m  .1�� � 1  16�
� 
ppgc� ��� l 88����  �  �  � ��� r  8A��� m  8;�� ���  U n m o u n t i n g   d i s k� 1  ;@�
� 
ppga� ��� I BI���
� .sysoexecTEXT���     TEXT� m  BE�� ��� > d i s k u t i l   e j e c t   / V o l u m e s / P I R A D A R�  � ��� r  JS��� m  JM�� � 1  MR�
� 
ppgc� ��� l TT����  �  �  � ��� r  T]��� m  TW�� ���  D o n e� 1  W\�
� 
ppga� ��� I ^c���
� .sysodelanull��� ��� nmbr� m  ^_�� �  � ��� l dd��
�	�  �
  �	  � ��� I du���
� .sysodisAaleR        TEXT� m  dg�� ��� B U S B   d i s k   f o r m a t t e d   w i t h   d a t a b a s e s� ���
� 
mesS� m  jm�� ��� � Y o u   m a y   n o w   s a f e l y   r e m o v e   t h e   U S B   d i s k   f r o m   y o u r   M a c   a n d   i n s e r t   i t   i n   t o   t h e   R a s p b e r r y   P i   r u n n i n g   P i - r a d a r .� ���
� 
btns� m  nq�� ���  O K�  � ��� l vv����  �  �  �  �u  �t  �v  ��   � k  ~��� ��� I ~�� ��
�  .sysodisAaleR        TEXT� m  ~��� ���   I n c o r r e c t   F o r m a t� ����
�� 
mesS� l �������� b  ����� b  ��   b  �� o  ������ 0 selecteddisk selectedDisk m  �� � "   i s   f o r m a t t e d   a s   o  ������ 0 diskfs diskFS� m  �� � � .   P l e a s e   f o r m a t   i t   a s   M S - D O S   ( F A T )   u s i n g   D i s k   U t i l i t y   t o   u s e   i t   h e r e .��  ��  � ��	
�� 
btns J  ��

  m  �� �  Q u i t �� m  �� � " O p e n   D i s k   U t i l i t y��  	 ����
�� 
dflt m  ������ ��  �  Z  ������ > �� l ������ n  �� 1  ����
�� 
bhit l ������ 1  ����
�� 
rslt��  ��  ��  ��   m  �� �  Q u i t O ��  I ��������
�� .miscactvnull��� ��� null��  ��    m  ��!!�                                                                                      @ alis    Z  Macintosh HD               ��BD ����Disk Utility.app                                               ������        ����  
 cu             	Utilities   1/:System:Applications:Utilities:Disk Utility.app/   "  D i s k   U t i l i t y . a p p    M a c i n t o s h   H D  .System/Applications/Utilities/Disk Utility.app  / ��  ��  ��   "��" l ����������  ��  ��  ��   �   end if disk is MS-DOS    � �## ,   e n d   i f   d i s k   i s   M S - D O S � $��$ l ����������  ��  ��  ��  ��  ��   �   end if disk exists    � �%% &   e n d   i f   d i s k   e x i s t s � &��& l ����������  ��  ��  ��   g '(' = ��)*) o  ������ 0 dbmenureturn dbMenuReturn* m  ��++ �,, $ L o a d   C u s t o m   R o u t e s( -��- k  ��.. /0/ I ����12
�� .sysodisAaleR        TEXT1 m  ��33 �44 $ L o a d   C u s t o m   R o u t e s2 ��56
�� 
mesS5 m  ��77 �88 � P l e a s e   v i e w   t h e   i n s t r u c t i o n s   b e f o r e   c o n t i n u i n g   t o   l o a d   a   c u s t o m   r o u t e   d a t a b a s e   f o r   a n   a i r l i n e6 ��9��
�� 
btns9 J  ��:: ;<; m  ��== �>> " V i e w   I n s t r u c t i o n s< ?��? m  ��@@ �AA  C o n t i n u e��  ��  0 BCB Z  ��DE��FD = ��GHG l ��I����I n  ��JKJ 1  ����
�� 
bhitK l ��L����L 1  ����
�� 
rslt��  ��  ��  ��  H m  ��MM �NN  C o n t i n u eE k  �pOO PQP r  �RSR I �����T
�� .sysostdfalis    ��� null��  T ��UV
�� 
prmpU m  �WW �XX ~ S e l e c t   t h e   c u s t o m   a i r l i n e   r o u t e   d a t a b a s e   y o u   w o u l d   l i k e   t o   l o a dV ��Y��
�� 
ftypY m  ZZ �[[  c s v��  S o      ���� 0 customroutes customRoutesQ \]\ I (��^��
�� .sysoexecTEXT���     TEXT^ b  $_`_ b   aba m  cc �dd  c p  b n  efe 1  ��
�� 
strqf l g����g n  hih 1  ��
�� 
psxpi o  ���� 0 customroutes customRoutes��  ��  ` m   #jj �kk ,   / t m p / r o u t e s C U S T O M . c s v��  ] lml r  )Lnon l )Hp����p n  )Hqrq 1  DH��
�� 
ttxtr l )Ds����s I )D��tu
�� .sysodlogaskr        TEXTt m  ),vv �ww Z E n t e r   t h e   t h r e e - d i g i t   c a l l s i g n   o f   t h e   a i r l i n eu ��xy
�� 
dtxtx m  /2zz �{{  y ��|}
�� 
disp| m  58��
�� stic   } ��~
�� 
btns~ m  9<�� ���  C o n t i n u e �����
�� 
dflt� m  =>���� ��  ��  ��  ��  ��  o o      ���� 0 callsign  m ��� Z  Mn������ = MT��� o  MP���� 0 callsign  � m  PS�� ���  B A W� I W\������
�� .sysodlogaskr        TEXT��  ��  ��  � I _n�����
�� .sysoexecTEXT���     TEXT� b  _j��� b  _f��� m  _b�� ��� H m v   / t m p / r o u t e s C U S T O M . c s v   / t m p / r o u t e s� o  be���� 0 callsign  � m  fi�� ���  . c s v��  � ���� l oo��������  ��  ��  ��  ��  F k  s��� ��� r  s���� c  s���� n  s���� 1  ����
�� 
psxp� l s������� I s�����
�� .sysorpthalis        TEXT� m  sv�� ��� F C r e a t i n g   c u s t o m   r o u t e   d a t a b a s e s . p d f� �����
�� 
in B� l y������� I y������
�� .earsffdralis        afdr� m  y|���                                                                                      @ alis    �  Macintosh HD               ��BD ����Pi-radar Utility.app                                           ������        ����  
 cu             utility   K/:Users:jackwoodward:Documents:ADS-B receiver:utility:Pi-radar Utility.app/   *  P i - r a d a r   U t i l i t y . a p p    M a c i n t o s h   H D  HUsers/jackwoodward/Documents/ADS-B receiver/utility/Pi-radar Utility.app  /    ��  ��  ��  ��  ��  ��  ��  � m  ����
�� 
TEXT� o      ���� $0 instructionspath instructionsPath� ��� I �������
�� .aevtodocnull  �    alis� o  ������ $0 instructionspath instructionsPath��  � ���� l ����������  ��  ��  ��  C ��� l ����������  ��  ��  � ���� l ����������  ��  ��  ��  ��  ��   c   end if dbMenu    d ���    e n d   i f   d b M e n u a ���� l ����������  ��  ��  ��  ��  ��   /   end if main menu    0 ��� "   e n d   i f   m a i n   m e n u��       ������  � ��
�� .aevtoappnull  �   � ****� �����������
�� .aevtoappnull  �   � ****� k    ���  ��  -����  ��  ��  � ���� 0 disk  � � �� # ' *��������~ 6 < C Q X [�} j q�| u x ��{�z�y�x�w�v�u ��t ��s�r�q�p�o�n�m ��l ��k � ��j ��i�h'�g4�f�eB�dO�cT�b�a�`�_�^\^jw�]����������\����[����!�Z+37=@MW�YZ�X�Wcjv�Vz�U�T��S�R�Q�����P�O
�� 
btns
�� 
dflt�� 
�� .sysodisAaleR        TEXT
� 
bhit�~  0 mainmenureturn mainMenuReturn�} 0 dbmenureturn dbMenuReturn
�| 
mesS
�{ .sysoexecTEXT���     TEXT
�z 
cpar�y 0 disklist diskList�x 0 filtereddisks filteredDisks
�w 
kocl
�v 
cobj
�u .corecnte****       ****
�t 
prmp
�s 
inSL
�r 
mlsl
�q 
empL�p 
�o .gtqpchltns    @   @ ns  �n 0 
chosendisk 
chosenDisk�m 0 selecteddisk selectedDisk
�l 
strq�k 0 diskfs diskFS�j 0 
diskparent 
diskParent�i 
�h 
rslt
�g 
ppgt
�f 
ppgd
�e 
ppgc
�d 
ppga
�c 
in B
�b .earsffdralis        afdr
�a .sysorpthalis        TEXT
�` 
psxp
�_ 
TEXT�^ *0 callsignfetcherpath callsignFetcherPath�] 0 routesbawpath routesBAWPath�\ 
�[ .sysodelanull��� ��� nmbr
�Z .miscactvnull��� ��� null
�Y 
ftyp
�X .sysostdfalis    ��� null�W 0 customroutes customRoutes
�V 
dtxt
�U 
disp
�T stic   
�S .sysodlogaskr        TEXT
�R 
ttxt�Q 0 callsign  �P $0 instructionspath instructionsPath
�O .aevtodocnull  �    alis��������mv�m� �,E�O��  �j OPY��� ����lv�l� �,E` O_ a  �a a a �a � Oa j a -E` OjvE` O -_ [a a l kh  �a  �_ 6FY h[OY��O_ a a  a !jva "fa #fa $ %E` &O_ &f_ &a k/E` 'Oa (_ 'a ),%a *%j E` +Oa ,_ 'a ),%a -%j E` .O_ +a / sa 0a a 1_ '%a 2%�a 3a 4_ '%lv�ka 5 O_ 6�,a 7<a 5*a 8,FOa 9*a :,FOj*a ;,FOa <*a =,FOa >a ?a @j Al Ba C,a D&E` EOa F_ E%a G%j Ok*a ;,FOa H*a =,FOa Ia ?a @j Al Ba C,a D&E` JOa K_ J%a L%j Ol*a ;,FOa M*a =,FOa Nj Om*a ;,FOa O*a =,FOa P_ .%j O�*a ;,FOa Q*a =,FOa Rj Oa Sj Oa T*a ;,FOa U*a =,FOa Vj Oa 5*a ;,FOa W*a =,FOkj XOa Ya a Z�a [� OPY hY Ga \a _ 'a ]%_ +%a ^%�a _a `lv�la 5 O_ 6�,a a a b *j cUY hOPOPY hOPY �_ a d  �a ea a f�a ga hlv� O_ 6�,a i  z*a a ja ka l� mE` nOa o_ na C,a ),%a p%j Oa qa ra sa ta u�a v�ka $ wa x,E` yO_ ya z  
*j wY a {_ y%a |%j OPY )a }a ?a @j Al Ba C,a D&E` ~O_ ~j OPOPY hOPY hascr  ��ޭ