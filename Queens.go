package main
import(
	"fmt";
	"math/rand";
	"time"
)
const n int =25
const numQueens int =n
const boardLen int =n
const numMaxPossibilities int =(boardLen-1)*numQueens
func printBoard(state [numQueens]int){
	fmt.Println()
	for i:=0;i<2*n-1;i++{
		fmt.Printf("-")
	}
	fmt.Println()
	fmt.Println()
	for i:=0;i<boardLen;i++{
		for j:=0;j<boardLen;j++{
			if state[j]==i{
				fmt.Printf("Q ")
			}else{
				fmt.Printf(". ")
			}
		}
		fmt.Println()
	}
	fmt.Println()
	for i:=0;i<2*n-1;i++{
		fmt.Printf("-")
	}
	fmt.Println()
}
func main(){	
	t0 := time.Now()
	state:= takeAleatoryPosic()
	//printBoard(state)
	answ, answH:=takeHillClimbing(state)	
	var candidate [numQueens]int
	var candidateH int
	for ;answH!=0;{
		state:= takeAleatoryPosic()
		candidate, candidateH=takeHillClimbing(state)
		if candidateH<answH{
			answ, answH=candidate,candidateH
		}
	}	
	t1 := time.Now()
	fmt.Printf("\nFoi encontrada a seguinte solucao, apos %v\n", t1.Sub(t0))	
	printBoard(answ)
	fmt.Print("nenhum ataque para ",numQueens," rainhas\n\n")
}
func takeHillClimbing(original [numQueens]int) ([numQueens]int, int){
	before:=copyState(original)
	current, currentH:=hillClimbing(before)
	for ;current!=before;{
		before=current
		current, currentH=hillClimbing(before)
	}
	return current, currentH
}
func hillClimbing(original [numQueens]int) ([numQueens]int, int){
	currentState:=copyState(original)
	currentH := calculateH(currentState)
	locals:= possibleStates(currentState)
	for i:=0; i<len(locals);i++{
		//printBoard(locals[i])
		neighborState :=locals[i]
		neighborH := calculateH(neighborState)
		//fmt.Print(neighborH)
		if neighborH < currentH{
			currentState=neighborState
			currentH=neighborH
		}
	}	
	//fmt.Print("\n",currentH)
	return currentState, currentH
}
func possibleStates(state [numQueens]int) [][numQueens]int{
	slice_possibleStates:= make([][numQueens]int, 0, numMaxPossibilities)
	copy_:=copyState(state)
	for i:=0;i<numQueens;i++{
		aux:=copyState(copy_)
		for j:=0;j<boardLen;j++{
			if copy_[i]!=j {
				aux[i]=j
				slice_possibleStates = Extend(slice_possibleStates, aux)
			}
		}
	}
	return slice_possibleStates
}

func Extend(slice [][numQueens]int, element [numQueens]int) [][numQueens]int {
    n := len(slice)
    slice = slice[0 : n+1]
    slice[n] = element
    return slice
}
func calculateH(state [numQueens]int) int{
	h:=0
	for i:=0;i<numQueens;i++{
		for j:=i+1;j<numQueens;j++{
			if isAttacked(state[i], i,state[j], j){
				h++
			}
		}
	}
	return h
}
func isAttacked(pos1X int, pos1Y int, pos2X int, pos2Y int) bool{
	//same line
	if pos1X==pos2X{
		return true
	}
	//same column
	if pos1Y==pos2Y{
		return true
	}
	//same ascending diag 
	if pos1X+pos1Y == pos2X + pos2Y{
		return true
	}
	//same descending diag
	if pos1X-pos2X == pos1Y-pos2Y{
		return true
	}
	return false
}
func takeAleatoryPosic() [numQueens]int{
	var state [numQueens]int
	for i:=0;i<numQueens;i++{
		state[i]=-1
	}
	var index int
	index=0
	for ;index<numQueens;{		
		random:=rand.Intn(boardLen)
		if state[random]==-1{
			state[index]=random
			index++
		}
	}
	return state;
}
func copyState(state [numQueens]int)[numQueens]int{
	var copy_ [numQueens]int
	for i:=0;i<numQueens;i++{
		copy_[i]=state[i]
	}
	return copy_
}