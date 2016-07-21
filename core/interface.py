#!/usr/bin/env python2.7
#coding=UTF-8

# Copyright (c) 2016 Angelo Moura
#
# This file is part of the program PytheM
#
# PytheM is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from modules.utils import *
from jarvis import Jarvis
from modules.completer import Completer
import os
import termcolor
import readline

class Processor(object):

	def __init__(self):
		self.arpmode = "rep"
		self.Jarvis = Jarvis()
		self.targets = None
		self.file = None
		self.interface = None
		self.gateway = None
		self.status = 0
		self.dnsstat = 0
		#will need to add a set and print, utils and wiki commands reference too
		self.port = 80
		self.domain = None
		self.redirect = None
		self.script = None


	def start(self):
		try:
			while 1:
				completer = Completer("pythem")
				console = termcolor.colored("pythem>","red", attrs=["bold"])
				self.command = raw_input("{} ".format(console))
				self.argv = self.command.split()
				self.input_list = [str(a) for a in self.argv]
				try:

					if self.input_list[0] == "help":
						print_help()
		
					elif self.command == "jarvis":
						self.Jarvis.start('core/processor.py')
	                                        self.status = 1						

					elif self.input_list[0] == "jarvis":
						if self.input_list[1] == "log":
							try:
								jarvislog = self.input_list[2]
								try:
									os.system("tail -f log/jarvis{}.txt".format(jarvislog))
								except Exception as e:
									print "[!] Exception caught: {}".format(e)
									pass

							except IndexError:
								print "[+] Jarvis log system."
								print "[.] Error log  - type: err"
								print "[.] Output log - type: out"
								try:
									jarvislog = raw_input("[+] Select: ")
									os.system("tail -f log/jarvis{}.txt".format(jarvislog))
								except KeyboardInterrupt:
									pass
								except Exception as e:
									print "[!] Exception caught: {}".format(e)
									pass

						elif self.input_list[1] == "help":
							jarvis_help(self.Jarvis.version)

						elif self.input_list[1] == "say":
							try:
								message = self.input_list[2]
								all_msg = " ".join(self.input_list[2:])
								self.Jarvis.Say(all_msg)
							except IndexError:
								try:
									message = raw_input("[+] Jarvis speaker: ")
									self.Jarvis.Say(message)
								except KeyboardInterrupt:
									pass
							except Exception as e:
								print "[!] Exception caught: {}".format(e)

						elif self.input_list[1] == "read":
							try:
								file = self.input_list[2]
								self.Jarvis.Read(file)
							except IndexError:
								if self.file is not None:
									self.Jarvis.Read(self.file)
								else:
									file = "[+] Set file path:"
									pass
                                                	except TypeError:
                                                		print "[!] You probably forgot to set a wordlist file path."
                                                	        pass
							except KeyboardInterrupt:
								pass
							except Exception as e:
								print "[!] Exception caught: {}".format(e)
	
						else:
							self.Jarvis.start('core/processor.py')
	                                                self.status = 1

					elif self.command == "exit" or self.command == "quit":
						if self.status == 1:
							self.Jarvis.Say(self.Jarvis.random('salutes'))
							self.Jarvis.stop()
							exit()
						else:
							exit()

					
					elif self.input_list[0] == "set" or self.input_list[0] == "SET":
						if self.input_list[1] == "interface":
							try:
								self.interface = self.input_list[2]
							except IndexError:
								try:
									self.interface = raw_input("[+] Enter the interface: ")
								except KeyboardInterrupt:
									pass
						elif self.input_list[1] == "port":
							try:
								self.port = int(self.input_list[2])
							except IndexError:
								try:
									self.port = input("[+] Enter the default port: ")
								except KeyboardInterrupt:
									pass

						elif self.input_list[1] == "domain":
							try:
								self.domain = self.input_list[2]
							except IndexError:
								try:
									self.domain = raw_input("[+] Domain to be spoofed: ")
								except KeyboardInterrupt:
									pass

						elif self.input_list[1] == "redirect":
							try:
								self.redirect = self.input_list[2]
							except IndexError:
								try:
									self.redirect = raw_input("[+] IP address to redirect DNS queries: ")
								except KeyboardInterrupt:
									pass

						elif self.input_list[1] == "script":
							try:
								self.script = self.input_list[2]
							except IndexError:
								try:
									self.script = raw_input("[+]Script url/path: ")
								except KeyboardInterrupt:
									pass


						elif self.input_list[1] == "gateway":
							try:
								self.gateway = self.input_list[2]
							except IndexError:
								try:
									self.gateway = raw_input("[+] Enter the gateway: ")
								except KeyboardInterrupt:
									pass
						elif self.input_list[1] == "target":
							try:
								self.targets = self.input_list[2]
							except IndexError:
								try:
									self.targets = raw_input("[+] Enter the target(s): ")
								except KeyboardInterrupt:
									pass
						elif self.input_list[1] == "file":
							try:
								self.file = self.input_list[2]
							except IndexError:
								try:
									self.file = raw_input("[+] Enter the path to the file: ")
								except KeyboardInterrupt:
									pass
						elif self.input_list[1] == "arpmode":
							try:
								self.arpmode = self.input_list[2]
							except IndexError:
								try:
									self.arpmode = raw_input("[+] Enter the arpmode:")
								except KeyboardInterrupt:
									pass

						else:
							print "[!] Select a valid variable to set."


					elif self.input_list[0] == "print":
						if self.input_list[1] == "interface":
							print "[+] Network Interface: {}".format(self.interface)
						elif self.input_list[1] == "port":
							print "[+] Default port: {}".format(self.port)
						elif self.input_list[1] == "domain":
							print "[+] Domain: {}".format(self.domain)
						elif self.input_list[1] == "redirect":
							print "[+] Redirecting to: {}".format(self.redirect)
						elif self.input_list[1] == "script":
							print "[+] Script url/path: {}".format(self.script)
						elif self.input_list[1] == "gateway":
							print "[+] Gateway IP Address: {}".format(self.gateway)
						elif self.input_list[1] == "target":
							print "[+] Target(s): {}".format(self.targets)
						elif self.input_list[1] == "file":
							print "[+] File path: {}".format(self.file)
						elif self.input_list[1] == "arpmode":
							print "[+] ARP spoofing mode: {}".format(self.arpmode)
						else:
							print "[-] Select a valid variable name."

					elif self.input_list[0] == "scan":
						try:
							mode = self.input_list[1]
							if self.targets is not None and self.interface is not None:
								from modules.scanner import Scanner
								self.scan = Scanner(self.targets, self.interface, mode)
								self.scan.start()
							else:
								print "[!] You probably forgot to set the interface or a valid IP address/range."
						except IndexError:
							try:
								print "[*] Select one scan mode, options = tcp/arp/manual"
								mode = raw_input("[+] Scan mode: ")
							except KeyboardInterrupt:
								pass
							if self.targets is not None and self.interface is not None:
								from modules.scanner import Scanner
								self.scan = Scanner(self.targets, self.interface, mode)
								self.scan.start()
							else:
								print "[!] You probably forgot to set the interface or a valid IP address/range."
								pass
						except KeyboardInterrupt:
							pass
						except Exception as e:
							print "[!] Exception caught: {}".format(e)
							pass

					elif self.input_list[0] == "arpspoof":
                                        	try:
					                myip = get_myip(self.interface)
                					mymac = get_mymac(self.interface)
                                                	from modules.arpoisoner import ARPspoof

							if self.input_list[1] == "start":
								self.spoof = ARPspoof(self.gateway, self.targets, self.interface,self.arpmode ,myip, mymac)
								self.spoof.start()
								print "[+] ARP spoofing initialized."

							elif self.input_list[1] == "stop":
								self.spoof.stop()
								print "[+] ARP spoofing finalized."

							else:
								print "[!] Select a valid option, call help to check syntax."
						
						except TypeError:
							print "[!] You probably forgot to set interface or gateway."
						except IndexError:
							print "[!] You probably forgot to type start or stop after arpspoof."
						except AttributeError:
							pass
						except Exception as e:
							print "[!] Exception caught: {}".format(e)

					elif self.input_list[0] == "dnsspoof":
						try:

							if self.input_list[1] == "start":
								if self.domain != None :
									domain = self.domain
								else:
									try: 
										domain = raw_input("[+] Domain to be spoofed: ")
										self.domain = domain
									except KeyboardInterrupt: pass

								if self.redirect != None:
									redirect = self.redirect
								else:
									myip = get_myip(self.interface)
									opt = raw_input("[+] Default address to redirect is:{} do you want to change?[y/n]".format(myip))
									if opt == "y" or opt == "Y" or opt == "yes" or opt == "YES": 
										try:redirect = raw_input("[+] IP address to be redirected: ")
										except KeyboardInterrupt: pass
									else:
										redirect = myip

								from modules.dnspoisoner import DNSspoof
								self.dnsspoof = DNSspoof(redirect)
								self.dnsspoof.start(domain,None)
								print "[+] DNS spoofing initialized"

							elif self.input_list[1] == "stop":
								self.dnsspoof.stop()
								print "[+] DNS spoofing finalized"
							else:
								print "[!] Select a valid option, call help to check syntax."
						except IndexError:
							print "[!] You probably forgot to type start or stop after dnsspoof."
						except Exception as e:
							print "[!] Exception caught: {}".format(e)

					elif self.input_list[0] == "inject":
						try:
							myip = get_myip(self.interface)
							if self.input_list[1] == "start":
								try:
									from modules.inject import Inject
									self.inject = Inject(myip,self.port,self.script)
									self.inject.server()
								except Exception as e:
									print "[!] Exception caught: {}".format(e)

							elif self.input_list[1] == "stop":
								try:
									self.inject.stop()
								except Exception as e:
									print "[!] Exception caught: {}".format(e)
							else:
								print "[!] You need to start or stop the inject module."
						except TypeError:
							print "[!] You probably forgot to type start or stop after inject."
						except Exception as e:
							print "[!] Exception caught: {}".format(e)

					elif self.input_list[0] == "sniff":
						from modules.sniffer import Sniffer
						try:
							filter = " ".join(self.input_list[1:])
							self.sniff = Sniffer(self.interface, filter)
							self.sniff.start()
						except IndexError:
							filter = raw_input("[+] Enter the filter: ")
                                                	self.sniff = Sniffer(self.interface, filter)
                                                	self.sniff.start()
						except KeyboardInterrupt:
                                                	pass

					elif self.command == "pforensic":
						try:
							completer = None
							completer = Completer("pforensic")
							from modules.pforensic import PcapReader
							self.pcapread = PcapReader(self.file)
							self.pcapread.start()
						except KeyboardInterrupt:
							pass
						except TypeError:
							print "[!] You probably forgot to set the .pcap file"
							pass
						except Exception as e:
							print "[!] Exception caught: {}".format(e)
							pass

					elif self.input_list[0] == "xploit":
						try:
							completer = None
							completer = Completer("xploit")
							from modules.exploit import Exploit
							if self.targets is not None and self.input_list[1] == "tcp":
								self.xploit = Exploit(self.targets, self.input_list[1])
								self.xploit.start()
							elif self.file is not None and self.input_list[1] == "stdin":
								self.xploit = Exploit(self.file, self.input_list[1])
								self.xploit.start()
							else:
								print "[!] You need to set or stdin or tcp as argument."
								print "[!] You need to set or a file or a target to xploit."
						except IndexError:
							try:
								print "[*] Select one xploit mode, options = stdin/tcp"
								mode = raw_input("[+] Exploit mode: ")
								if mode == "stdin" or mode == "tcp":
									from modules.exploit import Exploit
									if self.targets is not None:
										self.xploit = Exploit(self.targets, mode)
										self.xploit.start()
									elif self.file is not None:
										self.xploit = Exploit(self.file, mode)
										self.xploit.start()
									else:
										print "[!] You need to set or a file or a target to xploit."
								else:
									print "[!] Select a valid xploit mode, stdin or tcp"
							except KeyboardInterrupt:
								pass
                                                except TypeError:
                                                        print "[!] You probably forgot to set the file"
                                                        pass
                                                except KeyboardInterrupt:
                                                        pass
                                                except Exception as e:
                                                        print "[!] Exception caught: {}".format(e)
                                                        pass

					elif self.command == "cookiedecode":
						try:
							cookiedecode()
						except KeyboardInterrupt:
							pass
						except Exception as e:
							print "[!] Exception caught: {}".format(e)
							pass



					elif self.input_list[0] == "decode":
						try:
							print decode(self.input_list[1])
						except KeyboardInterrupt:
							pass


					elif self.input_list[0] == "encode":
						try:
							print encode(self.input_list[1])
						except KeyboardInterrupt:
							pass


					elif self.input_list[0] == "geoip":
						try:
							self.targets = self.input_list[1]
							from modules.geoip import Geoip
							path = "config/GeoLiteCity.dat"
							iptracker = Geoip(self.targets,path)

						except IndexError:
							if self.targets is not None:
								from modules.geoip import Geoip
								path = "config/GeoLiteCity.dat"
								iptracker = Geoip(self.targets,path)
							else:
								print "[!] You probably forgot to set a target"

						except Exception as e:
								print "[!] Exception caught: {}".format(e)
								pass

					elif self.input_list[0] == "brute":
							if self.input_list[1] == "ssh":
								try:
									username = raw_input("[+] Enter the username to bruteforce: ")
									from modules.ssh_bruter import SSHbrutus
									brutus = SSHbrutus(self.targets, username, self.file)
									brutus.start()
                                                		except KeyboardInterrupt:
                                                        		brutus.stop()
									pass
                                                		except TypeError:
                                                        		print "[!] You probably forgot to set the wordlist file path."
                                                       			pass
							elif self.input_list[1] == "url":
								try:
									url = 'url'
									from modules.web_bruter import WEBbrutus
									brutus = WEBbrutus(self.targets, self.file)
									brutus.start(url)
								except KeyboardInterrupt:
									brutus.stop(url)
									pass
								except TypeError:
			                                      		print "[!] You probably forgot to set the wordlist file path."
									pass
							elif self.input_list[1] == "form":
								try:
									form = 'form'
									from modules.web_bruter import WEBbrutus
									brutus = WEBbrutus(self.targets, self.file)
									brutus.start(form)
								except KeyboardInterrupt:
									brutus.stop(form)
									pass
								except TypeError:
		                                            		print "[!] You probably forgot to set the wordlist file path."
									pass
							else:
								print "[!] Select a valid type of brute-force type help to check."
					else:
						try:
							os.system("{}".format(self.command))
							pass
						except Exception as e:
							print "[!] Select a valid option, type help to check sintax."
							pass
				except IndexError:
					pass

				except Exception as e:
					print "Exception caught: {}".format(e)



		except KeyboardInterrupt:
			print "\n[*] User requested shutdown."
			exit()


