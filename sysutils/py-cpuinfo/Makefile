# $NetBSD: Makefile,v 1.3 2021/02/08 12:06:23 adam Exp $

DISTNAME=	py-cpuinfo-7.0.0
PKGNAME=	${PYPKGPREFIX}-${DISTNAME:S/py-//}
CATEGORIES=	sysutils python
MASTER_SITES=	${MASTER_SITE_PYPI:=p/py-cpuinfo/}

MAINTAINER=	pkgsrc-users@NetBSD.org
HOMEPAGE=	https://github.com/workhorsy/py-cpuinfo
COMMENT=	Get CPU info with pure Python
LICENSE=	mit

USE_LANGUAGES=	# none

post-install:
	cd ${DESTDIR}${PREFIX}/bin && ${MV} cpuinfo cpuinfo-${PYVERSSUFFIX} || ${TRUE}

.include "../../lang/python/egg.mk"
.include "../../mk/bsd.pkg.mk"
