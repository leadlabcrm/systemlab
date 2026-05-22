import os

html_path = '/Users/nithin/.gemini/antigravity-ide/scratch/systemlab/systemlab-v2.html'
with open(html_path, 'r') as f:
    html = f.read()

CSS = """
/* TEAM CSS */
.emp-avatar { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #000; flex-shrink: 0; }
.emp-row { display: flex; align-items: center; padding: 12px 14px; border-bottom: 1px solid var(--hairline); transition: background 0.1s; cursor: pointer; gap: 14px; }
.emp-row:hover { background: rgba(255,255,255,0.02); }
.emp-details { flex: 1; display: flex; flex-direction: column; gap: 2px; overflow: hidden; }
.emp-name { font-size: 13px; font-weight: 500; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.emp-role { font-size: 11px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.att-toggle { display: flex; background: var(--canvas-soft); border-radius: var(--r-pill); padding: 2px; gap: 2px; }
.att-btn { font-size: 10px; font-weight: 600; padding: 4px 10px; border-radius: var(--r-pill); cursor: pointer; color: var(--mute); transition: all 0.1s; user-select: none; border: none; background: transparent; }
.att-btn:hover { color: var(--body); }
.att-btn.present.active { background: rgba(34,197,94,0.15); color: var(--green); }
.att-btn.absent.active { background: rgba(239,68,68,0.15); color: var(--red); }
.team-stat-card { background: var(--canvas-card); border: 1px solid var(--hairline); padding: 16px; border-radius: var(--r-md); display: flex; flex-direction: column; gap: 4px; }
.team-stat-val { font-size: 24px; font-weight: 600; color: var(--ink); font-family: var(--f-mono, monospace); }
.team-stat-lbl { font-size: 11px; color: var(--mute); font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
"""

HTML_VIEWS = """
    <!-- TEAM VIEW -->
    <div id="v-team" class="view">
      <div class="dash-head" style="border-bottom:1px solid var(--hairline); padding-bottom:20px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-end;">
          <div>
            <div class="dash-h1">Team</div>
            <div class="dash-sub">Track daily attendance and active execution.</div>
          </div>
          <button class="btn btn-sm btn-primary" onclick="openAddEmpModal()">Add Employee</button>
        </div>
      </div>
      <div class="stats-row" id="team-stats" style="margin-bottom:24px;"></div>
      <div class="dash-body">
        <div class="panel-hd">Team Roster</div>
        <div id="team-roster" style="background:var(--canvas-card); border:1px solid var(--hairline); border-radius:var(--r-md); overflow:hidden;">
        </div>
      </div>
    </div>

    <!-- EMPLOYEE DETAIL VIEW -->
    <div id="v-employee" class="view">
      <div class="dash-head" style="border-bottom:1px solid var(--hairline); padding-bottom:20px; margin-bottom:20px; display:flex; gap:16px; align-items:center;">
        <button class="btn btn-xs btn-ghost" onclick="showView('team')" style="padding:4px"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg></button>
        <div id="emp-det-avatar" class="emp-avatar" style="width:40px;height:40px;font-size:16px;"></div>
        <div style="flex:1;">
          <div class="dash-h1" id="emp-det-name">Name</div>
          <div class="dash-sub" id="emp-det-role">Role</div>
        </div>
        <button class="btn btn-xs btn-danger" onclick="deleteEmployee()">Remove Employee</button>
      </div>
      <div class="dash-body">
        <div class="panel-hd">Recent Activity</div>
        <div id="emp-activity" style="padding:40px 0;">
          <div class="empty">
            <div class="empty-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            </div>
            <div style="font-weight:600;color:var(--body);margin-bottom:4px">No Activity Found</div>
            <div style="font-size:12px">This employee hasn't executed any SOPs recently.</div>
          </div>
        </div>
      </div>
    </div>
"""

HTML_MODAL = """
<!-- ADD EMPLOYEE MODAL -->
<div class="modal-overlay" id="add-emp-modal">
  <div class="modal" style="width:360px">
    <div class="modal-head">
      <div class="modal-title">Add Employee</div>
      <button class="btn btn-xs btn-ghost" onclick="closeAddEmpModal()">✕</button>
    </div>
    <div class="modal-body">
      <div class="field-group"><div class="field-lbl">Full Name</div><input type="text" id="newEmpName" placeholder="e.g. John Doe"></div>
      <div class="field-group"><div class="field-lbl">Role / Title</div><input type="text" id="newEmpRole" placeholder="e.g. Sales Associate"></div>
      <div class="field-group"><div class="field-lbl">Department</div>
        <select id="newEmpDept">
          <option value="">(None)</option>
        </select>
      </div>
    </div>
    <div class="modal-foot">
      <button class="btn btn-sm" onclick="closeAddEmpModal()">Cancel</button>
      <button class="btn btn-sm btn-primary" onclick="saveEmployee()">Add Employee</button>
    </div>
  </div>
</div>
"""

JS = """
// --- NATIVE TEAM LOGIC ---
const TT_TODAY = new Date().toISOString().split('T')[0];
const TT_COLORS = [
  {bg:'#fecaca',fg:'#991b1b'},{bg:'#fef08a',fg:'#854d0e'},{bg:'#bbf7d0',fg:'#166534'},
  {bg:'#bfdbfe',fg:'#1e40af'},{bg:'#e9d5ff',fg:'#6b21a8'},{bg:'#fbcfe8',fg:'#9d174d'}
];

function tt_col(i) { return TT_COLORS[i % TT_COLORS.length]; }
function tt_initials(n) { return n.split(' ').map(x=>x[0]).join('').substring(0,2).toUpperCase(); }

let curEmp = null;

function renderTeam() {
  if (!S.employees) S.employees = [];
  if (!S.att) S.att = {};
  
  const total = S.employees.length;
  const present = S.employees.filter(e => S.att[e.id] && S.att[e.id][TT_TODAY] === 'present').length;
  const absent = S.employees.filter(e => S.att[e.id] && S.att[e.id][TT_TODAY] === 'absent').length;
  
  document.getElementById('team-stats').innerHTML = `
    <div class="stat-cell"><div class="stat-n">${total}</div><div class="stat-lbl eyebrow">Total Members</div></div>
    <div class="stat-cell"><div class="stat-n" style="color:var(--green)">${present}</div><div class="stat-lbl eyebrow">Present Today</div></div>
    <div class="stat-cell"><div class="stat-n" style="color:var(--red)">${absent}</div><div class="stat-lbl eyebrow">Absent Today</div></div>
  `;
  
  let rosterHtml = '';
  if (total === 0) {
    rosterHtml = `<div style="padding:24px; text-align:center; color:var(--mute); font-size:13px;">No employees added yet.</div>`;
  } else {
    S.employees.forEach(e => {
      const c = tt_col(e.ci);
      const status = (S.att[e.id] && S.att[e.id][TT_TODAY]) || null;
      rosterHtml += `
        <div class="emp-row" onclick="openEmployee('${e.id}')">
          <div class="emp-avatar" style="background:${c.bg}; color:${c.fg}">${tt_initials(e.name)}</div>
          <div class="emp-details">
            <div class="emp-name">${e.name}</div>
            <div class="emp-role">${e.role || 'No Role'}</div>
          </div>
          <div class="att-toggle" onclick="event.stopPropagation()">
            <button class="att-btn present ${status==='present'?'active':''}" onclick="setAtt('${e.id}','present')">Present</button>
            <button class="att-btn absent ${status==='absent'?'active':''}" onclick="setAtt('${e.id}','absent')">Absent</button>
          </div>
        </div>
      `;
    });
  }
  document.getElementById('team-roster').innerHTML = rosterHtml;
}

function setAtt(eid, status) {
  if (!S.att[eid]) S.att[eid] = {};
  if (S.att[eid][TT_TODAY] === status) {
    delete S.att[eid][TT_TODAY]; // Toggle off
  } else {
    S.att[eid][TT_TODAY] = status;
  }
  if(window.persist) persist();
  renderTeam();
}

function openEmployee(eid) {
  curEmp = eid;
  const e = S.employees.find(x => x.id === eid);
  if (!e) return;
  const c = tt_col(e.ci);
  
  document.getElementById('emp-det-avatar').style.background = c.bg;
  document.getElementById('emp-det-avatar').style.color = c.fg;
  document.getElementById('emp-det-avatar').textContent = tt_initials(e.name);
  document.getElementById('emp-det-name').textContent = e.name;
  document.getElementById('emp-det-role').textContent = e.role || 'No Role';
  
  showView('employee', document.querySelector('.nav-item[data-view="team"]'));
}

function deleteEmployee() {
  if (!curEmp) return;
  requestConfirm("Remove Employee", "Are you sure? This cannot be undone.", () => {
    S.employees = S.employees.filter(x => x.id !== curEmp);
    delete S.att[curEmp];
    if(window.persist) persist();
    showView('team');
  });
}

function openAddEmpModal() {
  document.getElementById('newEmpName').value = '';
  document.getElementById('newEmpRole').value = '';
  const ds = document.getElementById('newEmpDept');
  ds.innerHTML = '<option value="">(None)</option>' + S.depts.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
  document.getElementById('add-emp-modal').classList.add('open');
  document.getElementById('newEmpName').focus();
}
function closeAddEmpModal() {
  document.getElementById('add-emp-modal').classList.remove('open');
}
function saveEmployee() {
  const name = document.getElementById('newEmpName').value.trim();
  const role = document.getElementById('newEmpRole').value.trim();
  const dept = document.getElementById('newEmpDept').value;
  if (!name) return showToast("Name is required", "error");
  
  S.employees.push({
    id: 'emp_' + Date.now().toString(36),
    name,
    role,
    dept,
    ci: Math.floor(Math.random() * TT_COLORS.length),
    joined: Date.now()
  });
  if(window.persist) persist();
  closeAddEmpModal();
  renderTeam();
}
"""

# Inject CSS exactly at APP SHELL
html = html.replace('/* APP SHELL */', f'{CSS}\n/* APP SHELL */')

# Inject HTML Views INSIDE #main exactly
target_views_loc = '  </div>\n</div>\n\n<!-- FLOWCHART MODAL -->'
html = html.replace(target_views_loc, f'{HTML_VIEWS}\n{target_views_loc}')

# Inject Modals
html = html.replace('<!-- TOAST -->', f'{HTML_MODAL}\n<!-- TOAST -->')

# Inject JS
html = html.replace('/* GO */', f'{JS}\n/* GO */')

# Add Team button to Sidebar
sidebar_btn = """        <div class="nav-item" data-view="team" onclick="showView('team',this)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          Team
        </div>\n"""
html = html.replace('Dashboard\n        </div>\n', f'Dashboard\n        </div>\n{sidebar_btn}')

# Hook into initialization and routing
html = html.replace('if (!S.depts) S.depts = [];', 'if (!S.depts) S.depts = [];\n  if (!S.employees) S.employees = [];\n  if (!S.att) S.att = {};')
html = html.replace("if (id==='dashboard') renderDashboard();", "if (id==='dashboard') renderDashboard();\n  if (id==='team') renderTeam();")

with open(html_path, 'w') as f:
    f.write(html)

print("Perfectly injected into pristine SystemLab.")
