<div style="text-align: right;">

# ממ"ן 11 – פתרון בעיית 8 האריחים באמצעות יוריסטיקה 

סטודנט: עומר שרייבשטיין\
אימייל: omershreib@gmail.com\
עדכון אחרון: 06/04/2026


***

### הערות לבודק הממן
1. קובץ זה נכתב במקור באנגלית (כי לנהל כתיבה של סמלים בעברית ובאנגלית זה סוג של עינוי), אולם כדי לעמוד בדרישות ההגשה שכוללות שהממן יהיה בעברית, יצרתי גרסה מצומצמת שרובה בעברית ומכילה את עיקר התוכן הנדרש מהמטלה. הגרסה באנגלית מעט עשירה יותר ולכן אני ממליץ לעבור גם עליה
2. קובץ זה מכיל תגיות markdown ו LaTex ולכן אני ממליץ לקרוא את הקובץ באמצעות Markdown Viewe, כמו זה ש Microsoft מציעה בחינם
https://apps.microsoft.com/detail/9p9sdhx8tqvq?hl=en-US&gl=IL
3. הוכחות, דוגמאות והגדרות מתמטיות השארתי באנגלית כי פשוט לא אפשרי לנהל תווים באנגלית ובעברית יחד באותה שורה בקובץ README מבלי שזה ייצא לא קריא לחלוטין
4. עך מנת להריץ את התוכנית צריך לוודא המצאות של הספריות הבאות, ובמידת הצורך להתקין אותם באופן הבא

</div>

```commandline
pip install matplotlib numpy
```

<div style="text-align: right;">

##  1 - סקירה כללית 

###  1.1 - ארכיטקטורה 

תוכנית זו מציעה מסגרת כללית לפתרון בעיות חיפוש באמצעות אלגוריתמי חיפוש 
 ופונקציות יוריסטיות, כנלמד בקורס מבוא לבינה מלאכותית.
ממן 11 עוסק בפתרון בעיית 8 האריחים על ידי כלים אלגוריתמים אלו.

:התוכנית מחולקת לשני חלקים עיקריים

#### מודולים כלליים (Reusable)


</div>

-   models/ -- מכילה מבני נתונים אבסטרקטיים כגון: Problem, State, Node
-   agents/ --  מכילה סוכנים המציעים לפתור בעיות, כל סוכן נעזר באלגוריתם חיפוש גרף או אסטרטגיה יוריסטית שונה
-   common.py -- מכילה כלים גלובלים בשימוש על ידי מודולים רבים
- search_strategies.py -- ("בשימוש על ידי כל סוכני ה"איי-סטאר) מכילה אסטרטגיות חיפוש


<div style="text-align: right;">
 
 על גבי אותם מודולים כלליים, תקיית

 `maman11\ ` 

 :מכילה את כל קבצי הקוד שמתמודדים באופן ישיר עם פתרון הבעיה של ממן זה, אלו כוללים

</div>

-   tiles_game_state.py
-   tiles_game_problem.py
-   tiles_evaluators.py
-   tiles.py

------------------------------------------------------------------------

<div style="text-align: right;">

שני עקרונות מרכזיים ניצבים בבסיס התכנון של תוכנית זו.
הראשון הוא היכולת לבצע שימוש חוזר בקוד באופן שישמש את כל הממנים התכנותיים,
 והשני הוא הפרדה לוגית בין לוגיקה כללית (כמו חיפוש) ללוגיקה ספציפית (כמו פתרון בעיית האריחים)



------------------------------------------------------------------------



### 1.4 - הרצה

</div>

``` bash
python -m introduction_to_AI.maman11.tiles <tiles...>
```

<div style="text-align: right;">

:דוגמה

</div>

``` bash
python -m introduction_to_AI.maman11.tiles 1 4 0 5 8 2 3 6 7
```

------------------------------------------------------------------------


<div style="text-align: right;">


## 2 - בעיית 8 האריחים: הגדרת הבעיה

כדי להגדיר באופן מיטבי את הבעיה, יש לפרט כיצד מתוארים המצב ההתחלתי ומצב היעד, כיצד מוגדרות הפעולות, מהו מודל המעברים וכיצד מוגדרת פונקציית המחיר 

### מצב התחלתי (דוגמה)

    [[6, 4, 8],
     [7, 5, 1],
     [2, 3, 0]]

### מצב יעד

    [[0, 1, 2],
     [3, 4, 5],
     [6, 7, 8]]

------------------------------------------------------------------------

### פעולות

:תנועה של אריח בכיוונים

LEFT, RIGHT, UP, DOWN

:בכתיב ווקטורי

</div>

- UP = [-1 0]
- DOWN = [+1 0]
- LEFT = [0 -1]
- RIGHT = [0 +1]


<div style="text-align: right;">

למעשה, פעולה על מצב נתון של המשחק (קרי, קונפיגורציה של האריחים) מוגדרת על ידי זוג (אריח, כיוון)

(מציין כי אלגנטי יותר להגדיר פעולה על ידי התנועה של הלוח הריק, במקום להסתכל על תנועת יתר האריחים, אבל שמתי לב לאופציה הזו בשלב מאוחר מדי...)



------------------------------------------------------------------------

### פונקציית המחיר

המחיר של כל הזזה חוקית של כל אריח שווה, כלומר אין מצב שבו הזזה של אריח מספר 2 תהיה יקרה יותר מזו של אריח מספר 3, 
כמו כן, כל הפעולות שוות במחירן (רוצה לומר, הזזת אריח למעלה אינה יקרה או זולה יותר מהזזה שמאלה)
 לכן פונקציית המחיר שווה ל-1, ומזה נובע כי המחיר משתלם (הזול) ביותר ממצב התחלתי כלשהו למצב היעד במשחק הוא המסלול הקצר ביותר, 
כלומר זה שדורש הזזה מינימאלית של אריחים

------------------------------------------------------------------------

### מודל המעברים

בתוכנית זו מודל המעברים ממומש בפועל על ידי המתודה

Problem.update(*state*, *action*)

מתודה זו מקבלת מצב קיים ופעולה ומחזירה מצב חדש שמתקבל מהמצב הקודם כתוצאה מאותה פעולה של הזזת אריח
 
לכל מצב נתון, קרי קונפיגורציית משחק נתונה, התמונה של המתודה מגדירה את מודל המעברים. 
זו מציגה את כל המצבים השכנים לאותו מצב נתון ושמתקבלים ממנה כתוצאה מהזזה חוקית של אריח.

:בתאור מתמטי

$$
T: STATES \times ACTIONS &rarr; STATES
$$

$$
T(state, action) = Problem.update(state, action) = newState 
$$

### מודל המעברים - דוגמה

</div>

```
state = [[0, 7, 8],    
        [2, 1, 5],   
        [6, 4, 3]]

Problem.get_actions(state) returns (in order): [(7, RIGHT), (2, UP)]

then, the image of the transition model when applied on this state looks as follows: 

                         [[7, 0, 8],    
T(state, (7, RIGHT))  ⟶  [2, 1, 5],   
                          [6, 4, 3]]


                      [[2, 7, 8],    
T(state, (2, UP))  ⟶  [0, 1, 5],   
                       [6, 4, 3]]

```

---

<div style="text-align: right;">


## 3 - אלגוריתמים

הממן מבקש להשוות בין מספר פתרונות מבוססי חיפוש לבעיית 8 האריחים - חיפוש לרוחב ועוד 2 פתרונות יוריסטיים מבוססי איי-סטאר

### BFS - סקירה כללית

חיפוש לרוחב תחילה הינו פתרון מבוסס חיפוש דטרמיניטי שמבטיח למצוא את המסלול האופטימלי (כלומר, הקצר ביותר) במידה והוא אכן קיים.
המימוש של חיפוש לרוחב תחילה מתבסס על תור FIFO. 
הבחירה במבנה נתונים זה מובילה לכך שילדי הצמתים של הרמה הנוכחית נכנסים ראשונים לתור, ולכן גם יצאו ממנו ויודפסו לפני הבנים שלהם הנמצאים ברמה הבאה (העמוקה יותר).
כפועל יוצא, אם בן של צומת ברמת עומק מסויימת מכיל את מצב המטרה, הסריקה תעצר את החיפוש בו לא תמשיך לפתח בנים של צמתים ברמה הבאה.

ישנם שני חסרונות עיקריים לחיפוש עומק. 
הראשונה היא שהיא מניחה כי משקלי כל הקשתות שווים, ולכן לא תומכת במצבים שבהם הנחה זו אינה מתקיימת. 
השנייה, בהתייחס לסיבוכיות מקום (זיכרון) היא שהאלגוריתם צורך זיכרון רב מכיוון שהוא דורש שמירה של כל הצמתים אותם פיתח בזיכרון. 
ראוי לציון כי בהשוואה לפתרונות יוריסטיים, חיפוש לרוחב מפתח כמות עצומה של צמתים, ולכן גם אינו כל כך יעיל אם לוקחים בחשבון סיבוכיות זמן.


### A* Search Based Heuristic

בחלק זה נבחן 2 דוגמאות לפתרונות יוריסטיים מבוססי איי-סאטר. בשעוסקים ביוריסטיקה יש שני דברים שחשוב לבדוק: קבילות ועקביות

</div>

Admissible:

$$h(n) ≤ h*(n)$$

Consistent:

$$h(n) ≤ c(n,a,n') + h(n')$$

<div style="text-align: right;">


.ראוי לציון כי עקביות היא תכונה חזקה יותר מקבילות ולכן עקביות גוררת קבילות (ההיפך לא נכון)
בנוסף, על פי הכתוב הספר הקורס (בעמודים 105-106) במידה ויוריסטיקה היא קבילה, אזי מובטח כי חיפוש איי-סטאר שמשתמש באותה יורסיטיקה תניב את הפתרון האופטימלי. 


### WrongRowCol (A*)

מדובר ביוריסטיקה שפיתחתי באופן עצמאי לחלוטין. 
זו מוגדרת על ידי סכימה של כל השורות והעמודות של כל האריחים שאינם נמצאים שורה/עמודת המטרה שלהם.
יוריסטיקה זו שואבת השראה ממרחק מנהטן, ובמידה מסויימת מציעה כלל אצבע פשטנית יותר. 

 בשונה ממרחק מנהטן שממש מחשב מרחק של כל אריח אל מקומו הנכון במצב המטרה,
היוריסטיקה שלי מעריכה את המרחק אל מצב המטרה על בסיס כל האריחים שנדרשים לזוז ממקומם הנוכחי, כאשר המונוטניות של יוריסטיקה זו באה לידי ביטוי בשאיפה לשפר את סך כל השורות + עמודות שגויות בכל מעבר בין מצב נתון למצב חדש. 

כלומר היוריסטיקה תעדיף להזיז אריח אל שורת/עמודת המטרה שלו.
יוריסטיקה זו מוכיחה כי אין צורך בחישוב מרחק כל אריח בכל מצב נתון כדי להגיע בסופו של דבר לפתרון אופטימלי. 
בחינה אמפירית מראה כי יוריסטיקה זו אומנם פחות דומיננטית על פני מרחק מנהטן (מפתחת יותר צמתים) אולם היא יותר דומיננטית ביחס ל

misplaced

:באופן מתמטי

</div>

$$h(n) := wrongRows + wrongColumns$$



#### Pseudo-Code

```
def wrong_row_col(state n, state s) {
   // retuns the total WrongRowCol score of state n
   //
   // args:
   //  n - the current state
   //  s - the goal state
   int score ⟵ 0;

   for each tile between 1 and 9 {
      int curr_x, curr_y ⟵ n.arg_pos(tile);
      int goal_x, goal_y ⟵ s.arg_pos(tile);

      if (curr_x != goal_x) then score++;
      if (curr_y != goal_y) then score++;
   }

   return score;
}
```


### Example Use Case:

```
state = [[0, 7, 8],    
        [2, 1, 5],   
        [6, 4, 3]]

sum of WrongRowCol's score according to the correct row+column of every tile

for example, tile #2 is located in position (1,0) while its goal position is (0,2), so both row and columns are wrong ==> +2
by another example, tile #7 is located in the correct row (1) but in the wrong column (0 != 2) ==> +1

                       [[ , +2, +1],    
 WrongRowCol(state) =  [+2, +1, 0],   = 8
                       [0, +1, +1]]
```
## WrongRowCol - Proof of Consistency:

Let tile *x* be located at position `(r_i,  c_k)` is state n, 
and suppose a single action causing *x* to move from row `r_i` to row `r_j`, producing state n'.

Only one tile moves, so:
- moving in/out to/from its goal row/column change WrongRowCol score by ±1
- diagonal movements are forbidden, and therefore only the row/column position can be changed between neighbors states

---

### Cases Analysis

#### Case 1: Neither `r_i` nor `r_j` is the goal row

Following this case scenario, the number of wrong rows and wrong columns remain the same - so:

$$h(n) - h(n') = 0 \leq 1$$

---

#### Case 2: `r_j` is the goal row (tile moves INTO goal row)

Following this case scenario, the number of wrong rows decreased by one (the number of wrong columns remain the same) - so:

$$h(n) - h(n') = (+1) \leq 1$$


#### Case 3: `r_i` is the goal row (tile moves OUT of goal row)

Following this case scenario, the number of wrong rows increased by one (the number of wrong columns remain the same) - so:

$$h(n) - h(n') = (-1) \leq 1$$


### Conclusion

In all cases:

$$h(n) - h(n') \leq 1$$

Therefore, the heuristic is consistent.

Since consistency implies admissibility, the heuristic is also admissible.

Q.E.D.

**Note:** 

1. the case where *x* moves vertically (between columns, instead of rows) is symmetrical.
2. as explained earlier, because *WrongRowCol* proved to be admissible, this A* search is also cost-optimal.

---


### LinearConflict (A*)

*" Starts with Manhattan distance, then for each row and column, the number of tiles
    \"in conflict\" are identified, and 2 * this number is added to the total distance.
    (It will take at least 2 additional moves to reshuffle the conflicting tiles into
    their correct positions.) This is an admissible improvement over
    Manhattan-Distance (`Hansson, Mayer, Young, 1985`)."*

Sources:
- Hansson, Mayer, Young, 1985: https://academiccommons.columbia.edu/doi/10.7916/D8154QZT/download
- Korf, Taylor, 1992: https://www.aaai.org/Library/AAAI/1996/aaai96-178.php

<div style="text-align: right;">

:ציטוט זה נמצא בקישור הנ"ל

</div>
*slidingtilepuzzle* python library: 

https://slidingtilepuzzle.readthedocs.io/en/latest/_modules/slidingpuzzle/heuristics.html#linear_conflict_distance

<div style="text-align: right;">

קונפליקט לינארי מציעה לשפר את מרחק מנהטן על ידי תוספת "ענישה" ליוריסטיקה מנהטן מחשבת.  

:בכתיב מתמטי

$$h(n) = MD(n) + LC(n)$$

(רצוי לעיין בהגדרות שמופיעות בהמשך חלק זה)

על פי 
`Korf` 
יוריסטיקה זו סיפקה את השיפור המשמעותי הראשון לבעיית האריחים ביחס למרחק מנהטן. 
 טרם פורסמה לראשונה ב-1985 מרחק מנהטן נחשב לפתרון היוריסטי הטוב ביותר שהיה ידוע לפתרון בעיית האריחים.  


:קונפליקט לינארי מוגדר באופן הבא 

</div>

let's have two tiles `t_j` and `t_k`. then, following the appearance of these 4 conditions:   
1. `t_j` and `t_k` are located in the same line (*i.e.*, same row or the same column)
2. the goal positions of `t_j` and `t_k` are both in that line.
3. `t_j` is to the **right** of `t_k`
4. in the goal state, `t_j` is to the **left** of `t_k`

<div style="text-align: right;">

רוצה לומר, קונפליקט לינארי עוסקת בבעייה שבא זוג אריחים נמצאים בשורת/עמודת המטרה שלהם אך הם ניצבים האחד מול השני ומהווים מכשול שמונע מכל אריח להגיע אל מקומו הנכון - ומזה נובע אותו קונפליקט.

`Hannson`

מספר במאמר שבו הציג את אותה יוריסטיקה כי הוא הגיעה לפיתוח שלה מתת-בעיה של מרחק מנהטן
שעוסק במציאת מסלול קצר ביותר וייחודי לכל אריח ביחס למקומו הנכון במצב היעד, 
הבסיס לקיומו של מקרה זה הוא רק כאשר אותו אריח כבר נמצא בשורה או בעמודת המטרה שלו, 
(relaxed problem) ולכן תחת פתרון בעיה רגועה יותר
של בעית האריחים, שבו אריחים לא מהווים מכשול אל היעד (כמו שקורה במנהטן) האריח פשוט צריך לנוע בקו ישר אל עבר 
מקומו הנכון.

 כאשר לוקחים בחשבון זוג אריחים הנתונים בקונפליקט לינארי, היוריסטיקה משערכת את מספר האריחים שנדרש להסיר מהלוח
על מנת לפתור את אותו קונפליקט ליניארי. 
כפועל יוצא נובע שעלות הטיפול בפתרון קונפליקט לינארי, המתבטא במספר הפעולות של הזזת אריח אל מקומו הנכון,  
הוא לכל הפחות **כפול** ממספר הפעולות המינימאלי שהיה נדרש לזוז אילולא הקונפליקט.  

</div>

#### LinearConflict - definitions:

MD(n) = sum of Manhattan distances  

lc(n, `r_i`) = the number of tiles that must be removed from row `r_i` in order to solve the linear conflict.  
lc(n, `c_i`) = the number of tiles that must be removed from column `c_i` in order to solve the linear conflict.  

LC(n) = estimated cost to solve all linear conflicts in this n-state. 

The lower bound of it is: 

$$LC(n) = 2 \times \sum_{0 \leq i \leq 2} [lc(n, r_i) + lc(n, c_i)]$$

the overall heuristic:

h(n) = MD(n) + LC(n)

The reason this **2** factor is because of *Corollary 5* in the `Hansson` paper claims that:

*"If there is a unique shortest path, p, between position X and position Y in the N 
Puzzle, then any alternate path will be at least 2 moves longer than p."*

---


#### Example Use Case:

```
state = [[0, 7, 8],    
        [2, 1, 5],   
        [6, 4, 3]]

ManhattanDistances(state) = 12

there are 3 linear conflicts:
(4,7), (1,7) and (8,5)

the minimum number of tiles required to be removed in order
to solve each of these linear conflicts is 1.according to Hannson, the lower bound
of the estimated cost to resolved a linear conflict, which in proportion to the tiles moves required to solve this linear conflict,
equals to doule the shortest path of each tiles towards their goal position in the relaxed problem (without any linear conflict)

therefore, these 3 linear confincts needed to be double in 2, resolving: LC(n) = 2*sum {0 <= i <= 2} [lc(n, r_i) + lc(n, c_i)]
in our example: LC(state) = 2*3 = 6

LinearConflict(state) = MD(state) + LC(state) = 12 + 2*3 = 12 + 6 = 18
```


## LinearConflict - Proof of Consistency: (based on the original proof written in the `Hansson` paper)

Let tile *x* be located at position `(r_i, c_k)` is state n, and suppose a single action causing *x* to move from row `r_i` to row `r_j`, producing state n'.

Only one tile moves, so:
- Manhattan distance changes by ±1
- Only affected rows/columns may change LC

---

### Key Property

For any row r:

$$lc(n', r) ∈ { lc(n, r), lc(n, r) ± 1 }$$

Therefore:

$$LC(n') - LC(n) ∈ {0, ±2}$$

---

### Cases Analysis

#### Case 1: Neither `r_i` nor `r_j` is the goal row

MD changes by ±1, LC unchanged:

$$h(n) - h(n') \leq 1$$

---

#### Case 2: `r_j` is the goal row (tile moves INTO goal row)

MD decreases by 1:

$$MD(n) - MD(n') = +1$$

LC may:
- stay the same → h(n) - h(n') = +1  
- increase by 2, resulting:

$$ 
\begin{aligned}
h(n) - h(n') &= MD(n) + LC(n) - [MD(n') + LC(n')] \newline
&= [MD(n) - MD(n')] + 2 \times \sum_{0 \leq i \leq 2} \left( [lc(n, r_i) + lc(n, c_i)] - [lc(n', r_i) + lc(n', c_i)] \right) \newline 
&= (+1) + 2 \times [lc(n, r_j) - lc(n', r_j)] \newline 
&= (+1) + 2 \times [lc(n, r_j) - (lc(n, r_j) + 1)] \newline
&= (+1) + 2 \times (-1) \newline
&= 1 - 2 \newline
&= (-1) \leq 1 \newline
\end{aligned} 
$$

Both satisfy consistency.

---

#### Case 3: `r_i` is the goal row (tile moves OUT of goal row)

MD increases by 1:

$$MD(n) - MD(n') = -1$$

LC may:
- stay the same → h(n) - h(n') = -1
- decrease by 2, resulting:

$$ 
\begin{aligned}
h(n) - h(n') &= MD(n) + LC(n) - [MD(n') + LC(n')] \newline
&= [MD(n) - MD(n')] + 2 \times \sum_{0 \leq i \leq 2} \left( [lc(n, r_i) + lc(n, c_i)] - [lc(n', r_i) + lc(n', c_i)] \right) \newline 
&= (-1) + 2 \times [lc(n, r_j) - lc(n', r_j)] \newline 
&= (-1) + 2 \times [lc(n, r_j) - (lc(n, r_j) - 1)] \newline
&= (-1) + 2 \times 1 \newline
&= (-1) + 2 \newline
&= (1) \leq 1 \newline
\end{aligned} 
$$

Both satisfy consistency.

---

### Conclusion

In all cases:

$$h(n) - h(n') \leq 1$$

Therefore, the heuristic is consistent.

Since consistency implies admissibility, the heuristic is also admissible.

Q.E.D.

**Note:** 

1. the case where *x* moves vertically (between columns, instead of rows) is symmetrical.
2. as explained earlier, because *LinearConflict* proved to be admissible, this A* search is also cost-optimal.

---


### דוגמת הרצה

```commandline
python -m introduction_to_AI.maman11.tiles 1 4 0 5 8 2 3 6 7
```

output:
 
```
algorithm: BFS
tiles path: [2, 8, 5, 3, 6, 7, 2, 8, 4, 1]
length: 10
expanded: 357
algorithm: wrong_row_col
tiles path: [2, 8, 5, 3, 6, 7, 2, 8, 4, 1]
length: 10
expanded: 12
algorithm: linear_conflict
tiles path: [2, 8, 5, 3, 6, 7, 2, 8, 4, 1]
length: 10
expanded: 10
```