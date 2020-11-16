1. 缩进语法
    1. 没有括号不容易发出编码风格的冲突
    2. 节省空间
        ```c
        void func(){
        }
        void func()
        {
        }
        ```
    3. 人性化
        ```c
        if (x <= y)
            x++;
            y--;
        z++ 
        ```

2. 为什么需要显示使用self
    由于Python没有声明，无法区分是局部变量赋值还是实例变量的属性赋值
    局部变量和实例变量存在于两个不同的命名空间中，您需要告诉 Python 使用哪个命名空间。
    ```python
    class T:
       def __init__(self, value):
           self.value = value
    ```
    ```cpp
    class Box
    {
       public:
          double length;      // 长度
          double breadth;     // 宽度
          double height;      // 高度
       
          double getVolume(void)
          {
             return length * breadth * height;  // 因此有些编码要求成员需要加m_前缀来区分
          }
    }; 
    ```
   
3. 如何管理内存
   Python的标准实现CPython使用引用计数来检测不可访问的对象，并使用另一种机制来收集引用循环，定期执行循环检测算法来查找不可访问的循环并删除所涉及的对象  
  
4. dict在CPython的实现
   字典的工作方式是使用 hash() 内置函数计算字典中存储的每个键的hash代码。hash代码根据键和每个进程的种子而变化很大；例如，"Python" 的hash值为-539294296，而"python"(一个按位不同的字符串)的hash值为1142331976。然后，hash代码用于计算内部数组中将存储该值的位置。假设您存储的键都具有不同的hash值，这意味着字典需要恒定的时间 -- O(1)，用Big-O表示法 -- 来检索一个键
   
   *为什么dict的key必须是不可变对象*
   字典的哈希表实现使用从键值计算的哈希值来查找键。如果键是可变对象，则其值可能会发生变化，因此其哈希值也会发生变化。当这个对象发生变化导致hash值发生变化，于是value可能不会对应之前的那个hash值
   