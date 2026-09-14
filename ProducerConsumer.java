class Buffer{
    int item;
    boolean hasItem =false;


synchronized void produce(int item) throws InterruptedException {
    while (hasItem){ 
    wait();  // wait if the buffer already has an item
    }
this.item=item;
hasItem=true;
System.out.println("Producer produced:" + item);
notify();//inform the consumer
}

synchronized void consume() throws InterruptedException{
    while(!hasItem){
        wait();
    }
    System.out.println("Consumer consumed:" + item);
    hasItem=false;
    notify();   //inform the producer
}
}
class Producer extends Thread{
    Buffer buffer;

    Producer(Buffer buffer){
        this.buffer=buffer;
    }

    public void run(){
        for(int i=1;i<=5;i++){
            try{
                buffer.produce(i);
            } catch (InterruptedException e){
                System.out.println(e);
            }
        }
    }
}

class Consumer extends Thread{
    Buffer buffer;

    Consumer(Buffer buffer){
        this.buffer=buffer;
    }
    public void run(){
        for(int i=1; i<=5;i++){
            try{
                buffer.consume();
            } catch(InterruptedException e){
                System.out.println(e);
            }
        }
    }
}
public class ProducerConsumer {
    public static void main(String[] args){
        Buffer buffer =new Buffer();

        Producer producer=new Producer(buffer);
        Consumer consumer=new Consumer(buffer);

        producer.start();
        consumer.start();
    }
}
