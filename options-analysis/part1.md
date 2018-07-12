# Разграничение привелегий:

User EXEC — пользовательский режим; по дефолту имеет «1» уровень привилегий;  
Privileged EXEC — привилегированый режим; имеет наивысший — «15» уровень привилегий;  
Global configuration — режим глобальной конфигурации;  

У Cisco всего есть 16 уровней привилегий — по нумерации от 0 до 15. Уровень «1» — дефолтный пользовательский, уровень «15» — высший привилегированный (полные права доступа).  

* Назначение пользователю уровня привилегий:  
`username user2 privilege 2 secret cisco`

* Задание соответствия между командами и уровнем привилегий:  
`privilege exec level 2 configure`  
`privilege exec level 2 configure t`  
`privilege configure level 2 interface`  
`privilege interface level 2 shutdown`  
`privilege interface level 2 ip address`  

* Задание пароля для входа в привилегированный режим 2 уровня:  
`enable secret level 2 ciscocisco`  



# AAA модель:

* Настройка AAA  
`aaa new-model`  
`aaa authentication login default local`  
`aaa authorization exec default local`  

* Назначение списка пользователю:  
`username xguru secret xguru`  
`username xguru aaa attribute list CLI`  

* Настроить ограничение количества попыток подключения, когда после определенного предела система заблокирует пользователя:  
`aaa local authentication attempts max-fail 5`  



# SSH/telnet:  

* Создание пары ключей (длина от 768 до 4096):  
`crypto key generate rsa modulus 1024`  

* Включение SSH версии 2:  
`ip ssh version 2`  

* Настройка VTY:  
`line vty 0 4`  
` login local`  
` transport input ssh`  

* Изменение порта SSH для определенной линии vty:  
`ip ssh port 2009 rotary 9`  
* Настройка соответствия vty и rotary:  
`line vty 4`  
` rotary 9`  

* Ограничение числа сессий ssh  
`ip ssh maxstartups 2`  

* Ограничение времени timeoutá (по-умолчанию 300 секунд)  
`ip ssh time-out 60`  

* Указание интерфейса для всех сессий ssh  
`ip ssh source-interface FastEthernet0/1`  

* Включение журналирования событий SSH ip ssh logging events  
`ip ssh logging events`  

* Настройка таймаута после которого, независимо от активности, пользователь будет отключен (в минутах):  
`line vty 0 15`  
` absolute-timeout 10`  

* Для ограничения доступа к маршрутизатору по протоколу telnet можно использовать ACL и применить их к vty.  
   Например, настроен ACL, который разрешает подключаться к маршрутизатору по telnet только с адреса 4.4.4.4:  
`access-list 10 permit 4.4.4.4`  
`line vty 0 4`  
` access-class 10 in`  

* Подключившись, например, с адреса 4.4.4.4 к маршрутизатору, можно затем из этой сессии инициировать сессию к другому маршрутизатору. Для того чтобы контролировать куда можно подключаться изнутри сессии необходимо настроить ACL в исходящем направлении. Например, подключившись к маршрутизатору, инициировать исходящую сессию можно будет только на адрес 1.1.1.1:  
`access-list 11 permit 1.1.1.1`  
`line vty 0 4`  
` access-class 11 out`  



# "Виды" паролей - какой тип, что обозначает. Какой безопасностью обладает:  

* Пользовательские пароли:  
Пользовательские пароли в конфигурационных файлах Cisco IOS зашифровано с помощью алгоритма, который является очень слабым по современным стандартам криптографии.  

* Пароли Enable Secret:  
Пароли enable secret закодированы с использованием алгоритма MD5.  

* Другие пароли:  
Почти все пароли и другие строки аутентификации пользователей в конфигурационных файлах закодированы слабым, обратимым алгоритмом, использованным для пользовательских паролей.  


* Пароль на консоль:  
`line console 0`  
` password MyPassword
` login

* Пароль на Telnet и SSH:
`line vty 0 4
` password MyPassword
` login

* Пароль на привилегированный режим:
`enable password MyEnablePassword
` или
`enable secret SecretPassword

* Задание минимальной длины пароля:
`security passwords min-length 6

* Хранение паролей в виде хеша:
`service password-encryption 

* Отключение функции восстановления пароля:
`no service password-recovery

* Задание количества разрешенных неудачных попыток логина в минуту. При превышении будет сгенерировано лог-сообщение:
`security authentication failure rate 3 log

* Задержка между попытками подключения (по умолчанию 1 секунда):
`login delay <sec>

* Логирование попыток подключения:
`login on-failure log [every <login-attempts>]
`login on-success log [every <login-attempts>]