# Фичи
* VTP (default, global)
По умолчанию switch является сервером, при этом в конфиге 
информации об этом нет. Здесь надо учитывать *шкалу 
защищенности(?) устройства*.  Если все же включено, то 
требуется создание vtp domain, password (нет в конфиге; 
mode,domain только в режиме off, transparent)
* DTP (default, local) 
switchport nonegotiate
* Storm control(local)
Два параметра: 1-порог, после которого срабатывает контроль, 
2-*приемлемый* уровень 
* STP (default, global)
 Защита:   
    - The Portfast feature, which disables spanning tree on a 
port.
    - The Root.BPDU guard feature
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
Требуется корректные дата и время
* Неиспользуемые порты shutdown



