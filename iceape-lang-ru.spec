%define	_lang	ru
%define	_reg	RU
%define	_lare	%{_lang}-%{_reg}
Summary:	Russian resources for Iceape
Summary(pl.UTF-8):	Rosyjskie pliki językowe dla Iceape
Name:		iceape-lang-%{_lang}
Version:	1.1.18
Release:	2
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		I18n
Source0:	http://releases.mozilla.org/pub/mozilla.org/seamonkey/releases/%{version}/contrib-localized/seamonkey-%{version}.%{_lare}.langpack.xpi
# Source0-md5:	f8b2711442d846bcc513018c8792d6b4
Source1:	http://www.mozilla-enigmail.org/download/release/0.96/enigmail-%{_lare}-0.96.xpi
# Source1-md5:	a90bceae5d78402e30973a67ee16cefb
Source2:	gen-installed-chrome.sh
URL:		http://www.seamonkey-project.org/
BuildRequires:	perl-base
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRequires:	zip
Requires(post,postun):	iceape >= %{version}
Requires(post,postun):	textutils
Requires:	iceape >= %{version}
Obsoletes:	seamonkey-lang-ru
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_chromedir	%{_datadir}/iceape/chrome

%description
Russian resources for Iceape.

%description -l pl.UTF-8
Rosyjskie pliki językowe dla Iceape.

%prep
%setup -q -c
%{__unzip} -o -qq %{SOURCE1}
install %{SOURCE2} .
./gen-installed-chrome.sh locale chrome/{%{_reg},%{_lare},%{_lang}-unix,enigmail-%{_lare}}.jar \
	> lang-%{_lang}-installed-chrome.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_chromedir}

install chrome/{%{_reg},%{_lare},%{_lang}-unix,enigmail-%{_lare}}.jar $RPM_BUILD_ROOT%{_chromedir}
install lang-%{_lang}-installed-chrome.txt $RPM_BUILD_ROOT%{_chromedir}
cp -r searchplugins dictionaries defaults $RPM_BUILD_ROOT%{_datadir}/iceape

# rebrand locale for iceape
cd $RPM_BUILD_ROOT%{_chromedir}
unzip %{_lare}.jar locale/%{_lare}/branding/brand.dtd locale/%{_lare}/branding/brand.properties \
	locale/%{_lare}/communicator/search/default.htm
sed -i -e 's/SeaMonkey/Iceape/g;' locale/%{_lare}/branding/brand.dtd \
	locale/%{_lare}/branding/brand.properties \
	locale/%{_lare}/communicator/search/default.htm
zip -0 %{_lare}.jar locale/%{_lare}/branding/brand.dtd locale/%{_lare}/branding/brand.properties \
	locale/%{_lare}/communicator/search/default.htm
rm -f locale/%{_lare}/branding/brand.dtd locale/%{_lare}/branding/brand.properties \
	locale/%{_lare}/communicator/search/default.htm

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	%{_sbindir}/iceape-chrome+xpcom-generate
fi

%postun
[ ! -x %{_sbindir}/iceape-chrome+xpcom-generate ] || %{_sbindir}/iceape-chrome+xpcom-generate

%files
%defattr(644,root,root,755)
%{_chromedir}/%{_reg}.jar
%{_chromedir}/%{_lare}.jar
%{_chromedir}/%{_lang}-unix.jar
%{_chromedir}/enigmail-%{_lare}.jar
%{_chromedir}/lang-%{_lang}-installed-chrome.txt
%{_datadir}/iceape/searchplugins/*
%{_datadir}/iceape/defaults/messenger/*.dat
%{_datadir}/iceape/defaults/messenger/%{_reg}
%{_datadir}/iceape/defaults/profile/%{_reg}
%{_datadir}/iceape/dictionaries/*