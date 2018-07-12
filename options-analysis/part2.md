# Работа с dhcp snooping
* описание  
фича предотвращает использование DHCP серверов на недоверенных интерфейсах, помогает бороться с MITM и DHCP starvation
также при использовании DHCP snooping, свитч начинает хранить информацию о соответствии mac адресу ip адреса
* синтаксис  
`(config-if)#ip dhcp snooping trust` - доверять данному интерфейсу (за ним DHCP сервер)
`(config-if)#ip dhcp snooping limit rate 10` - ограничение кол-ва клиентских запросов для недоверенных интерфейсов
`(config)#ip dhcp snooping vlan 13` - включение dhcp snooping для vlan 13
`(config)#ip dhcp snooping` - включение dhcp snooping глобально
# Защиты от arp spoofing
* arp inspection
	- описание  
	- синтаксис  
* arp guard
	- описание  
	- синтаксис  
# Port-security
* описание  
фича позволяет защищаться от атаки DHCP starvation (переполнение пула ip)
* синтаксис  
`(config-if)#switchport port-security` - включить опцию
`(config-if)#switchport port-security maximum 4` - 4 mac адреса на порт
`(config-if)#switchport port-security violation restrict` - при нарушении игнорировать лишние mac
`(config-if)#switchport port-security violation shutdown` - при нарушении выключить порт
`(config-if)#switchport port-security mac-address sticky` - порт запоминает разрешённые mac адреса
# Настройка vlan'ов
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
# best pratice по vlan/arp/dhcp
* статически настраивать режимы trunk/access
* не использовать native vlan