%define rubyver		1.9.3
%define rubyminorver	p194
%define rubyxver	1.9.1
%define sitedir         %{_libdir}/ruby/site_ruby
%define sitedir2        %{_prefix}/lib/ruby/site_ruby

Name:		ruby19
Version:	%{rubyver}%{rubyminorver}
Release:	1%{?dist}
License:	Ruby License/GPL - see COPYING
URL:		http://www.ruby-lang.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	readline readline-devel ncurses ncurses-devel gdbm gdbm-devel glibc-devel tcl-devel tk-devel libX11-devel autoconf gcc unzip openssl-devel db4-devel byacc make libyaml-devel
%ifnarch ppc64
BuildRequires:	emacs
%endif

Source0:	ftp://ftp.ruby-lang.org/pub/ruby/ruby-%{rubyver}-%{rubyminorver}.tar.bz2
# # for generating static reference manual (not used yet)
Source1:	bitclust-svn20120616.tar.bz2
Source2:	http://doc.ruby-lang.org/archives/201107/ruby-refm-1.9.2-dynamic-20110729.tar.gz
Source3:	http://ruby-doc.org/downloads/ruby_1_9_3_core_rdocs.tgz
# Ruby FAQ (obsoleted?)
Source4:	ftp://ftp.ruby-lang.org/pub/ruby/doc/rubyfaq-990927.tar.bz2
Source5:	ftp://ftp.ruby-lang.org/pub/ruby/doc/rubyfaq-jp-990927.tar.bz2
Source10:	ruby-mode-init.el


Summary:	An interpreter of object-oriented scripting language
Group:		Development/Languages
Provides:	ruby
Provides:	rubygems
Obsoletes:	ruby
Requires:	%{name}-libs = %{version}-%{release}

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.


%package libs
Summary:	Libraries necessary to run Ruby.
Group:		Development/Libraries
Provides:	ruby(abi) = %{rubyxver}
Provides:	ruby-libs
Provides:	libruby
Conflicts:	ruby(abi) < %{rubyxver}
Obsoletes:	ruby-libs
Obsoletes:	libruby

%description libs
This package includes the libruby, necessary to run Ruby.


%package devel
Summary:	A Ruby development environment.
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Provides:	ruby-devel
Obsoletes:	ruby-devel

%description devel
Header files and libraries for building a extension library for the
Ruby or an application embedded Ruby.


%package tcltk
Summary:	Tcl/Tk interface for scripting language Ruby.
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Provides:	ruby-tcltk
Obsoletes:	ruby-tcltk

%description tcltk
Tcl/Tk interface for the object-oriented scripting language Ruby.


%package irb
Summary:	The Interactive Ruby.
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Provides:	ruby-irb
Provides:	irb
Obsoletes:	ruby-irb
Obsoletes:	irb

%description irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.


%package rdoc
Summary:	A tool to generate documentation from Ruby source files
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-irb = %{version}-%{release}
Provides:	ruby-rdoc
Provides:	rdoc
Obsoletes:	ruby-rdoc
Obsoletes:	rdoc

%description rdoc
The rdoc is a tool to generate the documentation from Ruby source files.
It supports some output formats, like HTML, Ruby interactive reference (ri),
XML and Windows Help file (chm).


%package docs
Summary:	Manuals and FAQs for scripting language Ruby.
Group:		Documentation

%description docs
Manuals and FAQs for the object-oriented scripting language Ruby.


%ifnarch ppc64
%package mode
Summary:	Emacs Lisp ruby-mode for the scripting language Ruby
Group:		Applications/Editors
Requires:	emacs-common

%description mode
Emacs Lisp ruby-mode for the object-oriented scripting language Ruby.
%endif


%package ri
Summary:	Ruby interactive reference
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-rdoc = %{version}-%{release}
Provides:	ri
Provides:	ruby-ri
Obsoletes:	ri
Obsoletes:	ruby-ri

%description ri
ri is a command line tool that displays descriptions of built-in
Ruby methods, classes and modules. For methods, it shows you the calling
sequence and a description. For classes and modules, it shows a synopsis
along with a list of the methods the class or module implements.


%prep
%setup -q -c -a 3 -a 4 -a 5

%build
pushd ruby-%{rubyver}-%{rubyminorver}

rb_cv_func_strtod=no
export rb_cv_func_strtod
export CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing"

%configure \
  --with-default-kcode=none \
  --with-bundled-sha1 \
  --with-bundled-md5 \
  --with-bundled-rmd160 \
  --enable-shared \
  --enable-ipv6 \
%ifarch ppc
  --disable-pthread \
%else
  --enable-pthread \
%endif
  --with-lookup-order-hack=INET \
  --disable-rpath \
  --includedir=%{_includedir}/ruby \
  --libdir=%{_libdir}

%ifarch ppc
sed -i -e 's/^EXTMK_ARGS[[:space:]].*=\(.*\) --$/EXTMK_ARGS=\1 --disable-tcl-thread --/' Makefile
%endif
make RUBY_INSTALL_NAME=ruby %{?_smp_mflags}
%ifarch ia64
# Miscompilation? Buggy code?
rm -f parse.o
make OPT=-O0 RUBY_INSTALL_NAME=ruby %{?_smp_mflags}
%endif
%ifnarch ppc64
make test
%endif

popd

%install
rm -rf $RPM_BUILD_ROOT

%ifnarch ppc64
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/ruby-mode
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d
%endif

# installing documents and exapmles...
%{__mkdir_p} tmp-ruby-docs
pushd tmp-ruby-docs

# for ruby.rpm
%{__mkdir_p} ruby ruby-libs ruby-devel ruby-tcltk ruby-docs irb
pushd ruby
(cd ../../ruby-%{rubyver}-%{rubyminorver} && tar cf - sample) | tar xvf -
popd

# for ruby-libs
pushd ruby-libs
(cd ../../ruby-%{rubyver}-%{rubyminorver} && tar cf - lib/README*) | tar xvf -
(cd ../../ruby-%{rubyver}-%{rubyminorver}/doc && tar cf - .) | tar xvf -
(cd ../../ruby-%{rubyver}-%{rubyminorver} &&
 tar cf - `find ext \
  -mindepth 1 \
  \( -path '*/sample/*' -o -path '*/demo/*' \) -o \
  \( -name '*.rb' -not -path '*/lib/*' -not -name extconf.rb \) -o \
  \( -name 'README*' -o -name '*.txt*' -o -name 'MANUAL*' \)`) | tar xvf -
popd

# for irb
pushd irb
mv ../ruby-libs/irb/* .
rmdir ../ruby-libs/irb
popd

# for ruby-devel
pushd ruby-devel

popd

# for ruby-tcltk
pushd ruby-tcltk
for target in tcltklib tk
do
 (cd ../ruby-libs &&
  tar cf - `find . -path "*/$target/*"`) | tar xvf -
 (cd ../ruby-libs &&
  rm -rf `find . -name "$target" -type d`)
done
popd

# for ruby-docs
pushd ruby-docs
#{__mkdir_p} doc-en refm-ja faq-en faq-ja
%{__mkdir_p} doc-en faq-en faq-ja
(cd ../../ruby_1_9_3_core && tar cf - .) | (cd doc-en && tar xvf -)
## (cd ../../ruby-refm-ja && tar cf - .) | (cd refm-ja && tar xvf -)
(cd ../../rubyfaq && tar cf - .) | (cd faq-en && tar xvf -)
(cd ../../rubyfaq-jp && tar cf - .) | (cd faq-ja && tar xvf -)

(cd faq-ja &&
 for f in rubyfaq-jp*.html
 do
  sed -e 's/\(<a href="rubyfaq\)-jp\(\|-[0-9]*\)\(.html\)/\1\2\3/g' \
   < $f > `echo $f | sed -e's/-jp//'`
  rm -f $f; \
 done)
# make sure that all doc files are the world-readable
find -type f | xargs chmod 0644

popd

# fixing `#!' paths
for f in `find . -type f`
do
  sed -i -e 's,^#![     ]*\([^  ]*\)/\(ruby\|with\|perl\|env\),#!/usr/bin/\2,' $f
done

# done
popd

rubybuilddir=$RPM_BUILD_DIR/%{name}-%{version}/ruby-%{rubyver}-%{rubyminorver}
_cpu=`echo %{_target_cpu} | sed 's/^ppc/powerpc/'`

# installing binaries ...
make -C $rubybuilddir DESTDIR=$RPM_BUILD_ROOT install

# # generate static reference manual by bitclust
# LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} RUBYLIB=$RPM_BUILD_ROOT%{_libdir}/ruby/%{rubyxver}:$RPM_BUILD_ROOT%{_libdir}/ruby/%{rubyxver}/$_cpu-%{_target_os} $RPM_BUILD_ROOT/%{_bindir}/ruby -Ke ./bitclust/tools/bc-tohtmlpackage.rb -d ruby-refm-1.9.2-dynamic-20110729/db-1_9_2 -o html-1_9_2 --catalog=bitclust/data/bitclust/catalog

# generate ri doc
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} RUBYLIB=$RPM_BUILD_ROOT%{_libdir}/ruby/%{rubyxver}:$RPM_BUILD_ROOT%{_libdir}/ruby/%{rubyxver}/$_cpu-%{_target_os} make -C $rubybuilddir DESTDIR=$RPM_BUILD_ROOT install-doc

%{__mkdir_p} $RPM_BUILD_ROOT%{sitedir2}/%{rubyxver}
%{__mkdir_p} $RPM_BUILD_ROOT%{sitedir}/%{rubyxver}/$_cpu-%{_target_os}

%ifnarch ppc64
# installing ruby-mode
pushd ruby-%{rubyver}-%{rubyminorver}
cp misc/*.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/ruby-mode

## for ruby-mode
pushd $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/ruby-mode
cat <<EOF > path.el
(setq load-path (cons "." load-path) byte-compile-warnings nil)
EOF
emacs --no-site-file -q -batch -l path.el -f batch-byte-compile *.el
rm -f path.el*
popd
install -m 644 %{SOURCE10} \
        $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d

popd
%endif

# listing all files in ruby-all.files
(find $RPM_BUILD_ROOT -type f -o -type l) |
 sort | uniq | sed -e "s,^$RPM_BUILD_ROOT,," \
                   -e "s,\(/man/man./.*\)$,\1*," > ruby-all.files
egrep '(\.[ah]|libruby\.so)$' ruby-all.files > ruby-devel.files

# for ruby-tcltk.rpm
cp /dev/null ruby-tcltk.files
for f in `find ruby-%{version}/ext/tk/lib -type f; find ruby-%{version}/.ext -type f -name '*.so'; find ruby-%{version}/ext/tk -type f -name '*.so'`
do
  egrep "tcl|tk" ruby-all.files | grep "/`basename $f`$" >> ruby-tcltk.files || :
done

# for irb.rpm
fgrep 'irb' ruby-all.files > irb.files

# for ri
cp /dev/null ri.files
fgrep '%{_datadir}/ri' ruby-all.files >> ri.files
fgrep '%{_bindir}/ri' ruby-all.files >> ri.files

# for rdoc
cp /dev/null rdoc.files
fgrep rdoc ruby-all.files >> rdoc.files

# for ruby-libs
cp /dev/null ruby-libs.files
(fgrep    '%{_prefix}/lib' ruby-all.files;
 fgrep -h '%{_prefix}/lib' ruby-devel.files ruby-tcltk.files irb.files ri.files rdoc.files) | egrep -v "elc?$" | \
 sort | uniq -u > ruby-libs.files

%ifnarch ppc64
# for ruby-mode
cp /dev/null ruby-mode.files
fgrep '.el' ruby-all.files >> ruby-mode.files
%else
touch ruby-mode.files
%endif
# for ruby.rpm
sort ruby-all.files \
 ruby-libs.files ruby-devel.files ruby-tcltk.files irb.files ruby-mode.files ri.files rdoc.files |
 uniq -u > ruby.files

# for arch-dependent dir
rbconfig=`find $RPM_BUILD_ROOT -name rbconfig.rb`
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
export RUBYLIB=$RPM_BUILD_ROOT%{_libdir}/ruby/%{rubyxver}:$RPM_BUILD_ROOT%{_libdir}/ruby/%{rubyxver}/$_cpu-%{_target_os}
arch=`$RPM_BUILD_ROOT%{_bindir}/ruby -r $rbconfig -e 'printf("%s\n",RbConfig::CONFIG["arch"])'`
cat <<__EOF__ >> ruby-libs.files
%%dir %%{_libdir}/ruby/%%{rubyxver}/$arch
%%dir %%{_libdir}/ruby/%%{rubyxver}/$arch/digest
__EOF__

%clean
rm -rf $RPM_BUILD_ROOT
rm -f *.files
rm -rf tmp-ruby-docs

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%files -f ruby.files
%defattr(-, root, root)
%doc ruby-%{rubyver}-%{rubyminorver}/README
%lang(ja) %doc ruby-%{rubyver}-%{rubyminorver}/README.ja
%doc ruby-%{rubyver}-%{rubyminorver}/COPYING*
%doc ruby-%{rubyver}-%{rubyminorver}/ChangeLog
%doc ruby-%{rubyver}-%{rubyminorver}/LEGAL
%doc ruby-%{rubyver}-%{rubyminorver}/ToDo
%doc ruby-%{rubyver}-%{rubyminorver}/doc/NEWS*
%doc tmp-ruby-docs/ruby/*

%files devel -f ruby-devel.files
%defattr(-, root, root)
%doc ruby-%{rubyver}-%{rubyminorver}/README.EXT
%lang(ja) %doc ruby-%{rubyver}-%{rubyminorver}/README.EXT.ja

%files libs -f ruby-libs.files
%defattr(-, root, root)
%doc ruby-%{rubyver}-%{rubyminorver}/README
%lang(ja) %doc ruby-%{rubyver}-%{rubyminorver}/README.ja
%doc ruby-%{rubyver}-%{rubyminorver}/COPYING*
%doc ruby-%{rubyver}-%{rubyminorver}/ChangeLog
%doc ruby-%{rubyver}-%{rubyminorver}/LEGAL
%dir %{_libdir}/ruby
%dir %{_prefix}/lib/ruby
%dir %{_libdir}/ruby/%{rubyxver}
%dir %{_libdir}/ruby/%{rubyxver}/cgi
%dir %{_libdir}/ruby/%{rubyxver}/net
%dir %{_libdir}/ruby/%{rubyxver}/shell
%dir %{_libdir}/ruby/%{rubyxver}/uri
%{sitedir}
%{sitedir2}

%files tcltk -f ruby-tcltk.files
%defattr(-, root, root)
%doc tmp-ruby-docs/ruby-tcltk/ext/*

%files rdoc -f rdoc.files
%defattr(-, root, root)
%dir %{_libdir}/ruby
%dir %{_libdir}/ruby/%{rubyxver}

%files irb -f irb.files
%defattr(-, root, root)
%doc tmp-ruby-docs/irb/*
%dir %{_libdir}/ruby/%{rubyxver}/irb
%dir %{_libdir}/ruby/%{rubyxver}/irb/lc
%dir %{_libdir}/ruby/%{rubyxver}/irb/lc/ja

%files ri -f ri.files
%defattr(-, root, root)
%dir %{_datadir}/ri

%files docs
%defattr(-, root, root)
%doc tmp-ruby-docs/ruby-docs/*
%doc tmp-ruby-docs/ruby-libs/*

%ifnarch ppc64
%files mode -f ruby-mode.files
%defattr(-, root, root)
%doc ruby-%{rubyver}-%{rubyminorver}/misc/README
%dir %{_datadir}/emacs/site-lisp/ruby-mode
%endif

%changelog
* Sun Jun 24 2012 Yuji Abe <mechanicaljade@gmail.com> - 1.9.3p194-1
- bump the version to 1.9.3-p194
- separate packages like RHEL5
- add rubygems to Provides
- clean up spec file

* Tue Dec 27 2011 Rilindo Foster <rilindo.foster@monzell.com - 1.9.3-p0
- Update ruby version to 1.9.3-p0, made fork formal

* Mon Aug 29 2011 Gregory Graf <graf.gregory@gmail.com> - 1.9.2-p290
- Update ruby version to 1.9.2-p290

* Sat Jun 25 2011 Ian Meyer <ianmmeyer@gmail.com> - 1.9.2-p180-2
- Remove non-existant --sitearchdir and --vedorarchdir from %configure
- Replace --sitedir --vendordir with simpler --libdir
- Change %{_prefix}/share to %{_datadir}

* Tue Mar 7 2011 Robert Duncan <robert@robduncan.co.uk> - 1.9.2-p180-1
- Update prerequisites to include make
- Update ruby version to 1.9.2-p180
- Install /usr/share documentation
- (Hopefully!?) platform agnostic

* Sun Jan 2 2011 Ian Meyer <ianmmeyer@gmail.com> - 1.9.2-p136-1
- Initial spec to replace system ruby with 1.9.2-p136
