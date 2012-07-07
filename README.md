# What is this spec?

This spec is an attempt to push for a stable replacement of Ruby 1.8.x with 1.9.2+ on RHEL based systems.

### How to install

#### RHEL/CentOS 5/6

    yum install -y rpm-build rpmdevtools readline-devel ncurses-devel gdbm-devel tcl-devel openssl-devel db4-devel byacc
    rpmdev-setuptree
    yumdownloader --source ruby
    rpm -ivh ruby-1.8.5-*.src.rpm
    cd ~/rpmbuild/SOURCES
    wget http://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p194.tar.gz
    wget http://ruby-doc.org/downloads/ruby_1_9_3_core_rdocs.tgz
    wget http://doc.okkez.net/archives/201107/ruby-refm-1.9.2-dynamic-20110729.tar.gz
    wget http://ftp.ruby-lang.org/pub/ruby/doc/rubyfaq-990927.tar.gz
    wget http://ftp.ruby-lang.org/pub/ruby/doc/rubyfaq-jp-990927.tar.gz
    cd ~/rpmbuild/SPECS
    wget https://raw.github.com/yujiabe/ruby-1.9.x-rpm/master/ruby19.spec
    rpmbuild -bb ruby19.spec
    rpm -Uvh ~/rpmbuild/RPMS/x86_64/ruby19-1.9.3p194-1.x86_64.rpm ~/rpmbuild/RPMS/x86_64/ruby19-libs-1.9.3p194-1.x86_64.rpm ...

**PROFIT!**

### What it does

+ Builds
+ Split packages into ruby-libs, ruby-devel, etc
+ Installs
+ Overwrites/upgrades your currently installed ruby package (**DANGEROUS**)

### What it does **not** do

+ Install alongside Ruby 1.8.x

### TODO

+ Generates reference manual from ruby-refm-*-dynamic archive with bitclust
+ Rearrange package structure (to co-exist with Ruby 1.8.x packages)

### Requirements

+ EPEL Yum repository (for rpmdev-setuptree)

### Distro support

Tested working (as same as I could test for) on:

* CentOS 5.x x86_64

Not tested on:

* RHEL 5.x x86_64
* RHEL 6.x x86_64
* RHEL 6.x i686
* Scientific Linux 6.x x86_64
