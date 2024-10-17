Summary:	Validating XML Parser
Name:		xerces-c27
Version:	2.7.0
Release:	12
License:	ASL 2.0
Group:		System/Libraries
URL:		https://xml.apache.org/xerces-c/
Source0:        http://archive.apache.org/dist/xml/xerces-c/Xerces-C_2_7_0/source/xerces-c-src_2_7_0.tar.gz
Patch0:		xerces-c--CVE-2009-1885.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Xerces-C is a validating XML parser written in a portable subset of C++.
Xerces-C makes it easy to give your application the ability to read and write
XML data. A shared library is provided for parsing, generating, manipulating,
and validating XML documents. Xerces-C is faithful to the XML 1.0
recommendation and associated standards ( DOM 1.0, DOM 2.0. SAX 1.0, SAX 2.0,
Namespaces).

Note that this package contains Xerces-C++ 2.7.0 for compatibility with
applications that cannot use a newer version.


%package	devel
Summary:	Header files, libraries and development documentation for %{name}
Group:		Development/Java
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for xerces-c 2.7.0. If you like to develop programs using
xerces-c 2.7.0, you will need to install %{name}-devel.

%package doc
Group:		Development/Java
Summary:	Documentation for Xerces-C++ validating XML parser

%description doc
Documentation for Xerces-C++ 2.7.0.

Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.


%prep
%setup -q -n xerces-c-src_2_7_0
rm -rf doc/html/resources/.svn
find ./doc -type f -perm 755 -exec chmod 644 {} \;
find ./samples -type f -perm 755 -exec chmod 644 {} \;
%{__perl} -pi.orig -e 's|(PREFIX.)/lib\b|$1/%{_lib}|g' src/xercesc/configure */Makefile.in

iconv -f iso8859-1 -t utf-8 credits.txt > credits.txt.conv && mv -f credits.txt.conv credits.txt;
for i in feedback.xml migration.xml releases_archive.xml; do {
	iconv -f iso8859-1 -t utf-8 doc/$i > doc/$i.conv && mv -f doc/$i.conv doc/$i;
	};
done;

%patch0 -p0 -b .CVE-2009-1885


%build
export XERCESCROOT="$PWD"

# Let Makefiles be verbose
find -name 'Makefile.*' | while read f; do
	sed -i -e 's/$Q//g' \
	-e 's/{MAKE} -s/(MAKE)/g' \
	-e '/echo \"  (/d' \
	$f
done

# Remove conflicting flags from runConfigure
find -name runConfigure | while read f; do
	sed -i -e 's/-w -O -DNDEBUG/-DNDEBUG/g' $f
done

cd $XERCESCROOT/src/xercesc
%ifarch alpha ppc64 s390x sparc64 x86_64
CXXFLAGS="${RPM_OPT_FLAGS}" CFLAGS="${RPM_OPT_FLAGS}" ./runConfigure -plinux -cgcc -xg++ -minmem -nsocket -tnative -rpthreads -b64 -P %{_prefix} -C --libdir="%{_libdir}"
%else
CXXFLAGS="${RPM_OPT_FLAGS}" CFLAGS="${RPM_OPT_FLAGS}" ./runConfigure -plinux -cgcc -xg++ -minmem -nsocket -tnative -rpthreads -b32 -P %{_prefix} -C --libdir="%{_libdir}"
%endif
# not smp safe
%{__make}


%install
%{__rm} -rf $RPM_BUILD_ROOT
export XERCESCROOT="$PWD"
%{__make} install -C src/xercesc DESTDIR="$RPM_BUILD_ROOT"
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/xerces-c-2.7.0
cd $RPM_BUILD_ROOT%{_libdir}/xerces-c-2.7.0/
ln -s ../libxerces-c.so.27 libxerces-c.so
ln -s ../libxerces-depdom.so.27 libxerces-depdom.so
cd -
rm $RPM_BUILD_ROOT%{_libdir}/libxerces*.so
mkdir -p $RPM_BUILD_ROOT%{_includedir}/xercesc-2.7.0
mv $RPM_BUILD_ROOT%{_includedir}/xercesc $RPM_BUILD_ROOT%{_includedir}/xercesc-2.7.0


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_libdir}/libxerces*.so.*


%files devel
%defattr(0644,root,root,0755)
%dir %{_libdir}/xerces-c-2.7.0
%{_libdir}/xerces-c-2.7.0/libxerces*.so
%{_includedir}/xercesc-2.7.0/


%files doc
%defattr(0644,root,root,0755)
%doc Readme.html LICENSE NOTICE STATUS credits.txt doc samples




%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 2.7.0-11
+ Revision: 734286
- rebuild
- imported package xerces-c27

