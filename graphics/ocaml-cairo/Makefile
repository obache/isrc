# $NetBSD: Makefile,v 1.11 2021/04/21 11:41:57 adam Exp $

GITHUB_PROJECT=	ocaml-cairo
DISTNAME=	${GITHUB_PROJECT}-0.6.1
PKGREVISION=	8
CATEGORIES=	graphics
MASTER_SITES=	${MASTER_SITE_GITHUB:=Chris00/}

MAINTAINER=	jaapb@NetBSD.org
HOMEPAGE=	https://github.com/Chris00/ocaml-cairo/
COMMENT=	Bindings for OCaml to the cairo library
LICENSE=	gnu-lgpl-v3

USE_TOOLS+=	pkg-config

OCAML_USE_DUNE=		yes
OCAML_FINDLIB_DIRS=	cairo2 cairo2-gtk cairo2-pango
OPAM_INSTALL_FILES=	${OCAML_FINDLIB_DIRS}
DUNE_BUILD_PACKAGES=	${OCAML_FINDLIB_DIRS}

.include "../../mk/ocaml.mk"
.include "../../graphics/cairo/buildlink3.mk"
.include "../../devel/ocaml-dune-configurator/buildlink3.mk"
.include "../../x11/ocaml-lablgtk/buildlink3.mk"
.include "../../mk/bsd.pkg.mk"
