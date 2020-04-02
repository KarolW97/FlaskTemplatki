from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))

@bp.route("/cgi-bin/cm/secLoginPolicy/w_loginPolicy.html", methods=("GET", "POST"))
def w_loginPolicy():
    return render_template("/cgi-bin/cm/secLoginPolicy/w_loginPolicy.html")

@bp.route("/cgi-bin/cm/SNMPAgnt/w_g3admin.html", methods=("GET", "POST"))
def w_g3admin():
    return render_template("/cgi-bin/cm/SNMPAgnt/w_g3admin.html")

@bp.route("/cgi-bin/cm/secProtcls/w_protocols.html", methods=("GET", "POST"))
def w_protocols():
    return render_template("/cgi-bin/cm/secProtcls/w_protocols.html")

@bp.route("/cgi-bin/cm/secFirewall/w_lan_sec.html", methods=("GET", "POST"))
def w_lan_sec():
    return render_template("/cgi-bin/cm/secFirewall/w_lan_sec.html")

@bp.route("/cgi-bin/cm/SNMPTrap/w_configtrap.html", methods=("GET", "POST"))
def w_configtrap():
    return render_template("/cgi-bin/cm/SNMPTrap/w_configtrap.html")

@bp.route("/cgi-bin/cm/alrmSNMPAgents/w_SNMPAgents.html", methods=("GET", "POST"))
def w_SNMPAgents():
    return render_template("/cgi-bin/cm/alrmSNMPAgents/w_SNMPAgents.html")

@bp.route("/cgi-bin/cm/secServerAccess/w_serverAccess.html", methods=("GET", "POST"))
def w_serverAccess():
    return render_template("/cgi-bin/cm/secServerAccess/w_serverAccess.html")

@bp.route("/cgi-bin/cm/secFirewall/w_firewall.html", methods=("GET", "POST"))
def w_firewall():
    return render_template("/cgi-bin/cm/secFirewall/w_firewall.html")

@bp.route("/cgi-bin/cm/alrmSNMPTraps/w_SNMPTraps.html", methods=("GET", "POST"))
def w_SNMPTraps():
    return render_template("/cgi-bin/cm/alrmSNMPTraps/w_SNMPTraps.html")

@bp.route("/cgi-bin/cm/diagNetworkTimeSync/w_networkTimeSync.html", methods=("GET", "POST"))
def w_networkTimeSync():
    return render_template("/cgi-bin/cm/diagNetworkTimeSync/w_networkTimeSync.html")

@bp.route("/cgi-bin/cm/secModem/w_m_enable.html", methods=("GET", "POST"))
def w_m_enable():
    return render_template("/cgi-bin/cm/secModem/w_m_enable.html")

@bp.route("/cgi-bin/cm/secSyslog/w_syslogServer.html", methods=("GET", "POST"))
def w_syslogServer():
    return render_template("/cgi-bin/cm/secSyslog/w_syslogServer.html")

@bp.route("/cgi-bin/cm/filters/w_filtersadmin.html", methods=("GET", "POST"))
def w_filtersadmin():
    return render_template("/cgi-bin/cm/filters/w_filtersadmin.html")






