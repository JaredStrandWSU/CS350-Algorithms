Jared Strand 11463602
//For each pair(i, j) produced, in Python, convert it into 16 bits where the first 8 bits are for i in 8-bit insigned number, and the latter 8 bits are for j in 8-bit unsigned number.

//3) For each such 16 bits such as 10111011 10000110, convert this into a boolean expression in python, use library to create a boolean formula for the x and y values generated. (+ is for or, * is for and). Then use expr2bdd to convert the generated expression into a BDD.

//4) In python, to represent the boolean variables x1, x2, ... ,x8, y1, ... ,y8, z1, ... , z8; use a map
// xx1, xx2, ... , xx8, yy1, ... are BDD vars (use map)

//5)Create a d loop too
//bddr = the dijunction over all bdd's created in 3 ( the 'or' of all bdd's in 3)
//In python a disjunction uses the bddr.or() function and bdd's as params

//6)Repeat the loop until you have bddR6. Perfomr BDDR' compose BDDR'' by renaming the vars in BDDR' by doing bdd.compose() in python. Then you can perform the bdd.and() of BDDR' ^ BDDR''. Don't forget to perform bdd.smoothing() afterwards.

//////////////////////////////////////////////////////////////////
In the test.py (see below), ff is a BDD and aa is a bddvar, and 
ff.smoothing(aa)
will give you a BDD where the bddvar aa is eliminated existentially.

Hence, for the project, suppose that we are talking about the graph with four nodes.
You need two boolean variables for each node and define

f(a0,a1,b0,b1)

be the boolean formula representing the graph.  Consequently, we use 
ff
to denote the bdd of the f  (see the test.py code below to convert expr to bdd).

The f above essentially encodes the one-step reachability relation. To obtain two-step
version, you need the following boolean formula H


exists c0, c1.  f(a0,a1,c0,c1) \logic_and  f(c0,c1,b0,b1)


However, here, the key is to obtain the bdd denoted by HH  that represents the above formula H.
You need the following steps (totally four lines of code):

1. Create a BDD say FF1 for f(a0,a1,c0,c1), here you need use ff.compose(.....) medthod;
2. Create a BDD say FF2 for f(c0,c1,b0,b1), here you need use ff.compose(.....) medthod;
3. Create a BDD say FF3 for the logic_and of two BDDS FF1 and FF2;
4. Then, the desired HH is simply FF3.smoothing(cc0,cc1), where cc0 is the bddvar of the boolean var
c0, and so on.

You may write a loop to implement up to 5 step reachability relation.
To get final answer, you also need bdd.restrict method.


///////////////////////////////////////////////////////////////////////////////////// Test.py code
from pyeda.boolalg.bdd import (
    bddvar, bdd, expr2bdd, bdd2expr,
    BDDNODEZERO, BDDNODEONE, BDDZERO, BDDONE
)
from pyeda.boolalg.expr import exprvar, EXPRZERO, EXPRONE, Xor

x,y,z = map(exprvar, 'xyz')
xx,yy,zz = map(bddvar, 'xyz')
  
f = x*-y+-z   //boolean expression for (x and (not y)) or (not z)
    ff = expr2bdd(f)
        assert ff.smoothing(xx).equivalent(-yy.or(-zz))   //is this right???
  
        assert expr2bdd(x) == xx
  
        ff = expr2bdd(x*y+z)

        assert ff.restrict({}).equivalent(ff)
        assert ff.restrict({xx: 0}).equivalent(expr2bdd(z))   //plug-in false for bddvar xx
        assert ff.restrict({xx: 0, zz: 0}) is BDDZERO      //BDDZERO means false
  
        f = expr2bdd(x*y+z)
        ff = expr2bdd(yy*zz+xx)
        assert ff.compose({yy: xx, zz: yy, xx: yy}).equivalent(expr2bdd(f.compose({z: y})))  //variable renaming

///////////////////////////////////////////////////////////////////////////
1.
	R(x0,x1,x2,x3,x4,x5,x6,x7,x8, y0,y1,y2,y3,y4,y5,y6,y7,y8); //List of bool vars 256 node graph

	unsigned uint_8 i, j = bit(0);
															//	f = expr("a & b | a & c | b & c")
															//	>>> f
															//	Or(And(a, b), And(a, c), And(b, c))
															//	>>> f = expr2bdd(f)
															//	>>> f
															//	<pyeda.boolalg.bdd.BinaryDecisionDiagram at 0x7f556874ed68>
	while j <= 255
	{
		while i <= 255
		{
			if j - i > 0 && is_prime()
				//i is connected to j
				append(exprStr, R[i] + " & " + R[j] + " | "); 
			if i - j = 15
				//i is connected to j
				append(exprStr, R[i] + " & " + R[j] + " | "); 
			increment i
		}
	increment j
	}

	//create expression using expression string generated
	tmp = expr(exprStr);
	//create bddR from converted expression
	bddR = expr2bdd(tmp);

		bddR2 = bddR.compose(BddR);			//bddR6 of the Boolean formula R6 := R ◦ R ◦ R ◦ R ◦ R ◦ R ◦ R.
		bddR3 = bddR.compose(BddR2);
		bddR4 = bddR.compose(BddR3);
		bddR5 = bddR.compose(BddR4);
		bddR6 = bddR.compose(BddR5);

		//test equivalence										
		//SINCE
		In [1]: X = bddvars('x', 8)
		In [2]: f1 = X[0] & X[1] | X[2] & X[3] | X[4] & X[5]

		//NOTE on smoothing
		bdd.smoothing() for each bdd we create

		we can see the pattern as follows and determine if Ex. R6(x,x)
		a, b, c = map(bddvar, 'abc')
		f1 = a ^ b ^ c
		f2 = a & ~b & ~c | ~a & b & ~c | ~a & ~b & c | a & b & c

		//restriction

		//is Ex. R6(x,x) True? YES

		//STEPS
		Obtain the bddR
		Obtain the bddR6
		Perform quantifier elimination (compositions)
		Read pyeda documents until your head explodes
