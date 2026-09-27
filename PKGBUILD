# Maintainer: Saifan Ali Ayyat <saifanaliayyat@proton.me>
pkgname=guga
pkgver=1.0.0
pkgrel=1
pkgdesc="A lightweight Python AUR helper"
arch=('any')
url="https://github.com/void556/guga"
license=('MIT')
depends=('python' 'git' 'pacman')
source=("$pkgname-$pkgver.tar.gz::https://github.com/void556/guga/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir/$pkgname-$pkgver"
    install -Dm755 guga "$pkgdir/usr/bin/guga"
}
