# $NetBSD: Makefile,v 1.2 2021/04/24 19:44:52 pin Exp $

DISTNAME=	funst-0.1.1
CATEGORIES=	math
MASTER_SITES=	${MASTER_SITE_GITHUB:=sile/}

MAINTAINER=	pkgsrc-users@NetBSD.org
HOMEPAGE=	https://github.com/sile/funst/
COMMENT=	Tiny command-line tool to calculate fundamental statistics
LICENSE=	mit

.include "cargo-depends.mk"

USE_LANGUAGES+=	c

INSTALLATION_DIRS=	bin

do-install:
	${INSTALL_PROGRAM} ${WRKSRC}/target/release/funst ${DESTDIR}${PREFIX}/bin

.include "../../lang/rust/cargo.mk"
.include "../../mk/bsd.pkg.mk"
