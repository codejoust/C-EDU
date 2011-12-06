void print(char *in){
    while(*in != '\0'){
        putchar(*in);
        in++;
    }
}

int main(){
  print("Foo!");  
}