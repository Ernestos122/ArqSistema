#install.packages("glm")
library(glm2)
#Esto funciona, lo que exige solamente es que el train tenga un class label, llamado Risk en la seccion de entrenamiento.
#Hay que entrenar el modelo para luego testearlo. si es que el test se hara registro por registro, o todo un dataset, da lo mismo. 
# el output del modelo es la probabilidad de ser valor 1. 
# deje parametrizado el valor del threshold, para que se elija:
# si se pone threshold 0, el output es el resultado de probabilidad, por registro.
# si thres es cualquier valor mayor que 0, se pone valor 1 si es que el valor de probabilidad es mayor a ese threshold, y 0, en caso contrario.
# luego el threshold lo decidimos nosotros. lo dejare parametrizado con threshold para la toma de decision
RegLog <- function(thres){
  train<-read.csv2("trainSet.csv")
  test<-read.csv2("testSet.csv")
#fts<-as.formula(Risk~Visual + Text + Bot) #esto es por si solo tenia 3 variables, pero podria tener mas
fts<-as.formula(Risk~.)
model<-glm2(fts,family=binomial(link='logit'),data=train,control = list(1e-8, 1000, FALSE))
risk<-predict(model,newdata=test,type='response')
if(thres==0){
  return(risk)
  write.table(risk, "result.txt", append = FALSE, sep = " ", dec = "." )
  
}else{
  risk1<-ifelse(risk>=thres,1,0)
  write.table(risk1, "result.txt", append = FALSE, sep = " ", dec = "."  )
  
  return(risk1)
}
}
RegLog(0.48)
# el url deberia ser otro