# Девелоперский ридми #

# Roadmap:
- Сделать возвращение глобальных параметров и интерфейсов из parsing.py (сейчас они просто выводятся в консоль)
- Проверки  
- Цветной вывод результата (good, warning, bad)  
- Обернуть в установщик (setup.py)  
- Баннер  

# Что мы проверяем  
### Разграничение привелегий:

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



### AAA модель:

* Настройка AAA  
`aaa new-model`  
`aaa authentication login default local`  
`aaa authorization exec default local`  

* Назначение списка пользователю:  
`username xguru secret xguru`  
`username xguru aaa attribute list CLI`  

* Настроить ограничение количества попыток подключения, когда после определенного предела система заблокирует пользователя:  
`aaa local authentication attempts max-fail 5`  



### SSH/telnet:  

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



### "Виды" паролей - какой тип, что обозначает. Какой безопасностью обладает:  

* Пользовательские пароли:  
Пользовательские пароли в конфигурационных файлах Cisco IOS зашифровано с помощью алгоритма, который является очень слабым по современным стандартам криптографии.  

* Пароли Enable Secret:  
Пароли enable secret закодированы с использованием алгоритма MD5.  

* Другие пароли:  
Почти все пароли и другие строки аутентификации пользователей в конфигурационных файлах закодированы слабым, обратимым алгоритмом, использованным для пользовательских паролей.  


* Пароль на консоль:  
`line console 0`  
` password MyPassword`  
` login`  

* Пароль на Telnet и SSH:  
`line vty 0 4`  
` password MyPassword`  
` login`  

* Пароль на привилегированный режим:  
`enable password MyEnablePassword`  
 или  
`enable secret SecretPassword`  

* Задание минимальной длины пароля:  
`security passwords min-length 6`  

* Хранение паролей в виде хеша:  
`service password-encryption`  

* Отключение функции восстановления пароля:  
`no service password-recovery`  

* Задание количества разрешенных неудачных попыток логина в минуту. При превышении будет сгенерировано лог-сообщение:  
`security authentication failure rate 3 log`  

* Задержка между попытками подключения (по умолчанию 1 секунда):  
`login delay <sec>`  

* Логирование попыток подключения:  
`login on-failure log [every <login-attempts>]`  
`login on-success log [every <login-attempts>]`    

### Работа с dhcp snooping
* описание  
фича предотвращает использование DHCP серверов на недоверенных интерфейсах, помогает бороться с MITM и DHCP starvation
также при использовании DHCP snooping, свитч начинает хранить информацию о соответствии mac адресу ip адреса
* синтаксис  
`(config-if)#ip dhcp snooping trust` - доверять данному интерфейсу (за ним DHCP сервер)  
`(config-if)#ip dhcp snooping limit rate 10` - ограничение кол-ва клиентских запросов для недоверенных интерфейсов  
`(config)#ip dhcp snooping vlan 13` - включение dhcp snooping для vlan 13  
`(config)#ip dhcp snooping` - включение dhcp snooping глобально  

### Защиты от arp spoofing
* arp inspection
	- описание  
фича, привязывающая mac-ip к конкретному порту на свитче, использует таблицу dhcp snooping 
	- синтаксис  
`(config)#ip arp inspection vlan 13` - включение arp inspection для vlan 13
	- с использованием ACL вместо таблицы DHCP snooping  
`(config)#arp access-list <name>`
* source guard
	- описание  
фича, привязывающая mac-ip к конкретному порту на свитче, использует таблицу dhcp snooping 
	- синтаксис  
`(config-if)# ip verify source port-security`
	- без таблицы DHCP snooping  
`(config)# ip source binding <mac.add.ress> vlan <id> <IP.add.re.ss> interface <name>`

### Port-security
* описание  
фича позволяет защищаться от атаки DHCP starvation (переполнение пула ip)
* синтаксис  
`(config-if)#switchport port-security` - включить опцию  
`(config-if)#switchport port-security maximum 4` - 4 mac адреса на порт  
`(config-if)#switchport port-security violation restrict` - при нарушении игнорировать лишние mac  
`(config-if)#switchport port-security violation shutdown` - при нарушении выключить порт  
`(config-if)#switchport port-security mac-address sticky` - порт запоминает разрешённые mac адреса  

### Настройка vlan'ов
* native vlan
	- описание  
vlan, к которой причисляются все пакеты с портов, на которых явно не указаны vlan и 802.1 пакеты приходящие на trunk  
пакеты из native vlan, отправляемые через trunk также не сожержат заголовков 802.1q  
по умолчанию native vlan - vlan 1, можно задать кастомный номер
	- синтаксис  
`(config-if)#switchport trunk native vlan 7`
* access/trunk  
	- описание  
access - порт принимает пакеты 802.1 и отправляет далее по vlan этого порта. 
trunk - порт принимает пакеты 802.1q, отправляет пакеты в соответствующую vlan, если получен 802.1 пакет - отправляет его в native vlan.
можно (но не нужно) включать автоматическую настройку порта (dynamic)
	- синтаксис  
`(config-if)#switchport access vlan 11`  
`(config-if)#switchport mode trunk`
	- как не нужно делать  
`(config-if)#switchport mode dynamic desirable`  
`(config-if)#switchport mode dynamic auto`
* Защита от vlan hopping
	- описание  
vlan hopping - атака, позволяющая злоумышленнику покинуть пределы vlan.
	-защита  
для защиты от vlan hopping рекомендуется не использовать native vlan, а если очень хочется - хотя бы тегировать его в trunk
	- синтаксис  
`(config)#vlan dot1q tag native` - тегирование native vlan

### best pratice по vlan/arp/dhcp
* использовать arp inspection и source guard в связке с dhcp snooping
* адекватно разделять сеть на vlan'ы
* статически настраивать режимы trunk/access
* не использовать native vlan  

### IPv6 First Hop Security
[Cisco wiki](http://docwiki.cisco.com/wiki/FHS)
* RA guard  
Router Advertisement - DHCP для IPv6
	- простой случай (Дропаются все RA на интерфейсе)  
	`(config-if)#ipv6 nd raguard`
	- сложный случай  
```
	 !
  ipv6 nd raguard policy ONLY-DHCPv6-RAs
    ! role 'router' allows the RAs through but triggers deep inspection
     device-role router
    ! The RAs that we let through have to have Managed flag set.
     managed-config-flag on
    ! The Other configuration flag also needs to be set.
     other-config-flag on
    ! Only allow the RAs that advertise the prefixes from our own address space
    match ra prefix-list IPv6-SPACE
  !
  ! . . . 
  !
  interface Ethernet0/0
     description connection to R1 from Sw3
     switchport
     switchport access vlan 100
     switchport mode access
     ! Attach the policy to the port connecting to the router
     ipv6 nd raguard attach-policy ONLY-DHCPv6-RAs
     spanning-tree portfast
  !
  ! . . . 
  !
  ipv6 prefix-list IPv6-SPACE permit 2001:db8:cafe::/48 ge 64 le 64
```  

* Фрагментация  
Фрагментация пакетов [позволяет обходить](https://tools.ietf.org/html/draft-gont-v6ops-ra-guard-evasion-01) ra guard  
Ниже приведена конфигурация, позволяющая защититься от этой атаки  
```
!
interface GigabitEthernet1/0/1
 ipv6 traffic-filter nofrags in
!
ipv6 access-list nofrags
 deny ipv6 any FE80::/64 undetermined-transport
 permit ipv6 any any
!
```  

* IPv6 snooping
Network Discovery (IPv6 ARP) Inspection + RA guard + IPv6 address gleaning  
`(config)# ipv6 snooping policy ROUTER`  
`(config-ipv6-snooping)# device-role router`  
`(config)# ipv6 snooping policy HOST`  
На интерфейсе с роутером:  
`(config-if)#ipv6 nd raguard attach-policy ROUTER`  
На интерфейсе с хостами:  
`(config-if)#ipv6 nd raguard attach-policy HOST`  

* IPv6 source guard  
аналог ARP inspection
`(config)# ipv6 source-guard policy SG`  
`(config)# ipv6 source-guard attach-policy SG`  

### Фичи
* VTP (default, global)
Cлужит для работы(создание, удаление) VLANов.`Сервер может 
распространять информацию, о содержащихся в его базе VLANах, 
клиентам`.По умолчанию switch является сервером, при этом в конфиге
информации об этом нет. Здесь надо учитывать *шкалу
защищенности(?) устройства*.  Если все же включено, то
требуется создание vtp domain, password (нет в конфиге;
mode,domain только в режиме off, transparent)
* DTP (default, local)
`Динамическая настройка транков.`switchport nonegotiate
* Storm control(local)
Предотвращение широковещательного шторма.
Два параметра: 1-порог, после которого срабатывает контроль,
2-*приемлемый* уровень
* STP (default, global)
Устранение/предотвращение петель
 Защита:
    - The Portfast feature, which disables spanning tree on a
port.
    - The Root/BPDU guard feature
Loop Guard (предотвращает петли)
* CDP (default, global/local)
Информация об устройствах, подключенных к интерфейсам ( no
cdp enable -*local*;
no cdp run-*global*)
* Port security (local)
Позволяет указать MAC-адреса хостов/количество, которым
разрешено передавать данные через порт. *restrict ,
shutdown-оптимальные режимы реагирования на нарушение
безопасности*
* syslog(global)
Логи.Требуются корректные дата и время
* Неиспользуемые порты shutdown

|Features | default| global|interface|
| -- |:------:|:----| -:|
VTP|+|+||
DTP|+||+|
STORM|||+|
STP|+|+||
CDP|+|+|+|
DHCP SNOOP||+|+|
DAI||+|+|


### Фичи L3
1. HSRP(Hot Standby Router Protocol)
Служит для увеличения доступности шлюза по умолчанию. Объединяет     маршрутизаторы в группу и назначает им общий Ip-адрес.
`interface: standby [group-number] ip [ip-address [secondary]]`
*Возможна настройка аутентиикации с помощью пароля.*
Вся информация передается открытым текстом, установлен дефолтный пароль cisco. Имея параметры HSRP пакета, можно провести атаку, при этом роутер/L3 коммутатор злоумышленника станет активным. 
**Защита**: подсчет контрольной суммы с солью(секретный ключ). 
`interface: standby group authentication md5 key-string strongPASSWORD`  


# Файл "карта сети"
Файл, который описывает уровень доверия/критичности интерфейсов свича (+ 
какая-то дополнительная инофрмация ( которой не может быть в конфиге) о 
том как используется свич)
*Уровень доверия/Критичность: месторасположение, наличие СЗИ в сети, 
версия IOS устройства, является ли связующим звеном сети или служит 
только для подключения клиентов.*  

### Синтаксис: 
Руками указывать id vlan'ов 

critical_area: 1,5,7
unknown_area: 3,2,4
trusted_area: 8,9,10

* возможнность указать default area, для vlan присутстующих в конфигах, но не описанных в списке зон. По умолчанию они заносятся в самую "опасную" зону  *

# Ридми продакшена
# CCAT - Cisco Config Anaysis Tool #

# Usage  
`ccat -c example -vl vlmap.txt`  
# Installation  
`pip3 -r requirements.txt`  
`python3 setup.py install`  